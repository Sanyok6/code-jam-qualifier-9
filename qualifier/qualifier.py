import typing
from dataclasses import dataclass
import random

def find_staff_member(staff, speciality):
    availible = []

    for s in staff:
        for p in s.scope['speciality']:
            if p == speciality:
                availible.append(s)

    return random.choice(availible)


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]

class RestaurantManager:
    def __init__(self):
        self.staff = {}

    async def __call__(self, request: Request):
        request_type = request.scope['type']


        if request_type == 'staff.onduty':
            self.staff[request.scope['id']] = request

        if request_type == 'staff.offduty':
            self.staff.pop(request.scope['id'])

        if request_type == 'order':
            speciality = request.scope['speciality']

            selected = find_staff_member(self.staff.values(), speciality)

            full_order = await request.receive()
            await selected.send(full_order)

            result = await selected.receive()
            await request.send(result)

