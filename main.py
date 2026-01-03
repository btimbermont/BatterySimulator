import os
from dataclasses import dataclass
from typing import List, Dict

from battery_sim import Battery, ws_to_kwh, home_wizard_battery, marstek_venus

BATTERIES_TO_SIMULATE = {
    'Saldering': Battery(100000, 100000, 100000, 1.0),  # Saldering acts as a perfect infinite battery
    'HomeWizard x 1': home_wizard_battery(),
    'HomeWizard x 2': home_wizard_battery(2),
    'HomeWizard x 2 (eigen groep)': home_wizard_battery(2, True),
    'HomeWizard x 3': home_wizard_battery(3),
    'HomeWizard x 3 (eigen groep)': home_wizard_battery(3, True),
    'Marstek Venus': marstek_venus(False),
    'Marstek Venus (eigen groep)': marstek_venus(True),
    'Marstek Venus X2 (eigen groep)': marstek_venus(True,2),
}


@dataclass
class PowerDatapoint:
    time: int
    consumption: int
    production: int


def parse_mbc_file(path: str):
    with open(path) as file:
        for line in file.readlines():
            values = line.split()
            if len(values) != 3 or not values[0].isdigit():
                continue
            yield PowerDatapoint(int(values[0]), int(values[1]), int(values[2]))


def get_first_timestamp(path: str) -> int:
    with open(path) as file:
        for line in file.readlines():
            values = line.split()
            if len(values) != 3 or not values[0].isdigit():
                continue
            return int(values[0])


def simulate_battery(batteries: Dict[str, Battery], mbc_files: List[str]):
    previous_data = None
    consumption, production = 0, 0
    battery_results = {name: [0, 0] for name, _ in batteries.items()}
    for mbc_file in sorted(mbc_files, key=get_first_timestamp):
        for current_datapoint in parse_mbc_file(mbc_file):
            if previous_data is not None:
                duration = current_datapoint.time - previous_data.time
                if duration == 0:
                    # consecutive files have 1 overlapping data point, we can ignore this datapoint
                    ...
                elif current_datapoint.production > 0 and current_datapoint.consumption > 0:
                    # TODO: figure out what to do with this
                    # print(f'consumption and production at the same time is not supported!')
                    ...
                elif current_datapoint.production > 0:
                    # baseline
                    production += current_datapoint.production * duration
                    # with batteries
                    for name, battery in batteries.items():
                        if battery._available_capacity == 0:  # shortcut saves some time: full battery can't charge
                            battery_results[name][1] += current_datapoint.production * duration
                        else:
                            share_used = battery.charge(current_datapoint.production, duration)
                            battery_results[name][1] += (1 - share_used) * current_datapoint.production * duration
                elif current_datapoint.consumption > 0:
                    # baseline
                    consumption += current_datapoint.consumption * duration
                    # with batteries
                    for name, battery in batteries.items():
                        if battery._current_capacity == 0:  # shortcut saves some time: empty battery can't deliver power
                            battery_results[name][0] += current_datapoint.consumption * duration
                        else:
                            share_done_with_battery = battery.discharge(current_datapoint.consumption, duration)
                            battery_results[name][0] += (1 - share_done_with_battery) * current_datapoint.consumption * duration
            previous_data = current_datapoint
    print(f'Simulation done!')
    print(f'without battery: consumed {ws_to_kwh(consumption):.2f} kWh, produced {ws_to_kwh(production):.2f}kWh')
    print('With batteries:')
    for name, (consumption, production) in battery_results.items():
        print(f'{name}: consumed {ws_to_kwh(consumption):.2f} kWh, produced {ws_to_kwh(production):.2f}kWh')


if __name__ == '__main__':
    input_dir = 'input_2025'
    mbc_files = [f'{input_dir}/{f}' for f in os.listdir(input_dir)]
    simulate_battery(BATTERIES_TO_SIMULATE, mbc_files)
