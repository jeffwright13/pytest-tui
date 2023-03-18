import random

data = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nisl eget
vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed
auctor, nisl eget vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl
nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc nisl aliquam nisl,
eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc
nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget
vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed

Auctor, nisl eget vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl
nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc nisl aliquam nisl,
eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc
nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget
vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed

Nisl eget vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl apcemie
nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc nisl aliquam nisl,

eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget vulputate lacinia, nunc
nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed auctor, nisl eget
vulputate lacinia, nunc nisl aliquam nisl, eget aliquet nisl nisl sed nunc. Sed
"""

data_list = data.splitlines()


def fake_data(data=data_list) -> str:
    k = [random.choice(data_list) for _ in range(40)]
    return "\n".join(k)
