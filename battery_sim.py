def kwh_to_ws(kwh: float) -> int:
    return int(kwh * 1000 * 3600)


def ws_to_kwh(ws: int) -> float:
    return ws / (1000 * 3600)


class Battery:

    def __init__(self, capacity: float, max_charge_rate: int, max_discharge_rate: int, efficiency: float):
        self._capacity = kwh_to_ws(capacity)
        self._max_charge_rate = max_charge_rate
        self._max_discharge_rate = max_discharge_rate
        self._efficiency = efficiency
        self._current_capacity = 0

    @property
    def current_charge_in_kwh(self):
        return ws_to_kwh(self._current_capacity)

    @property
    def current_charge_in_percentage(self):
        return 100 * self._current_capacity / self._capacity

    @property
    def _available_capacity(self):
        return self._capacity - self._current_capacity

    def _add_capacity(self, capacity_in_ws: int):
        if capacity_in_ws <= self._available_capacity:
            self._current_capacity += capacity_in_ws
            return capacity_in_ws
        else:
            used_capacity = self._available_capacity
            self._current_capacity = self._capacity
            return used_capacity

    def charge(self, rate_in_w: int, duration_in_s: int) -> float:
        usable_rate_in_w = min(rate_in_w, self._max_charge_rate)
        available_capacity = int(usable_rate_in_w * duration_in_s * self._efficiency)
        stored_capacity = self._add_capacity(available_capacity)
        used_capacity = stored_capacity / self._efficiency
        return used_capacity / (rate_in_w * duration_in_s)

    def discharge(self, rate_in_w: int, duration_in_s: int):
        asked_capacity = rate_in_w * duration_in_s
        rate_in_w = min(rate_in_w, self._max_discharge_rate)
        capacity_given = min(rate_in_w * duration_in_s, self._current_capacity)
        self._current_capacity -= capacity_given
        return capacity_given / asked_capacity

    def __str__(self):
        return (f'Battery(total capacity: {ws_to_kwh(self._capacity)} kWh, '
                f'current charge: {self.current_charge_in_percentage:.2f}% ({self.current_charge_in_kwh} kWh))')


def home_wizard_battery(number_of_batteries: int = 1, own_group: bool = False):
    capacity = number_of_batteries * 2.7
    max_charge_rate = 800 * number_of_batteries
    efficiency = 0.8
    if own_group:
        max_discharge_rate = 800 * number_of_batteries
    else:
        max_discharge_rate = 800
    return Battery(capacity, max_charge_rate, max_discharge_rate, efficiency)
