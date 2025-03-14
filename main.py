import os
from dataclasses import dataclass
from typing import List

from battery_sim import Battery, ws_to_kwh, home_wizard_battery


@dataclass
class PowerDatapoint:
    time: int
    usage: int
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


def simulate_battery(battery: Battery, mbc_files: List[str]):
    previous_data = None
    consumption, production = 0, 0
    consumption_with_battery, production_with_battery = 0, 0
    for mbc_file in sorted(mbc_files, key=get_first_timestamp):
        for current_datapoint in parse_mbc_file(mbc_file):
            if previous_data is not None:
                duration = current_datapoint.time - previous_data.time
                if duration == 0:
                    ...
                elif current_datapoint.production > 0 and current_datapoint.usage > 0:
                    # print(f'consumption and production at the same time is not supported!')
                    ...
                elif current_datapoint.production > 0:
                    # baseline
                    production += current_datapoint.production * duration
                    # with battery
                    share_used = battery.charge(current_datapoint.production, duration)
                    production_with_battery += (1 - share_used) * current_datapoint.production * duration
                elif current_datapoint.usage > 0:
                    # baseline
                    consumption += current_datapoint.usage * duration
                    # with battery
                    share_done_with_battery = battery.discharge(current_datapoint.usage, duration)
                    consumption_with_battery += (1 - share_done_with_battery) * current_datapoint.usage * duration
            previous_data = current_datapoint
    consumption = ws_to_kwh(consumption)
    production = ws_to_kwh(production)
    consumption_with_battery = ws_to_kwh(consumption_with_battery)
    production_with_battery = ws_to_kwh(production_with_battery)
    print(f'Simulation done!')
    print(f'without battery: consumed {consumption:.2f} kWh, produced {production:.2f}kWh')
    print(f'with battery: consumed {consumption_with_battery:.2f} kWh, produced {production_with_battery:.2f}kWh')


if __name__ == '__main__':
    mbc_files = [f'input/{f}' for f in os.listdir('input')]
    battery = home_wizard_battery(1)
    simulate_battery(battery, mbc_files)
    battery = home_wizard_battery(2, True)
    simulate_battery(battery, mbc_files)
    battery = home_wizard_battery(3, True)
    simulate_battery(battery, mbc_files)
