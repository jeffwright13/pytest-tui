import pytest
import random


data = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    (
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut"
        " aliquip ex ea commodo consequat."
    ),
    (
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore"
        " eu fugiat nulla pariatur."
    ),
    (
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia"
        " deserunt mollit anim id est laborum."
    ),
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    (
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium"
        " doloremque laudantium."
    ),
    (
        "Totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi"
        " architecto beatae vitae dicta sunt explicabo."
    ),
    "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
    "Sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
    (
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur,"
        " adipisci velit."
    ),
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Nunc eget lorem ac lectus eleifend blandit.",
    "Aenean feugiat urna nec nulla ultrices consequat.",
    "Proin placerat odio a justo bibendum, ut dapibus nulla commodo.",
    "Vivamus et ultrices nunc, vitae tempus neque.",
    "Donec eget purus nec quam pretium mollis quis ut velit.",
    "Nam eu lacus euismod, sodales ipsum non, lacinia purus.",
    "Mauris varius sapien sed turpis congue, ac ullamcorper tortor tincidunt.",
    "Nam sit amet nisl vel purus dignissim blandit.",
    "Vivamus volutpat tristique ante quis vestibulum.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    (
        "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac"
        " turpis egestas."
    ),
    "Duis ut commodo risus, non fringilla justo.",
    "Praesent commodo commodo est, at maximus metus bibendum vitae.",
    "Donec eu justo ut massa posuere semper sit amet quis arcu.",
    "Proin eu est vel risus varius commodo id ut enim.",
    (
        "Morbi ornare, nisi vel consectetur bibendum, nibh elit mollis quam, ac"
        " vestibulum velit est at turpis."
    ),
    (
        "Donec finibus, sapien eget facilisis ultricies, velit risus faucibus lorem,"
        " euismod efficitur quam mauris ut turpis."
    ),
    "Ut commodo augue ut eros malesuada, vitae elementum risus suscipit.",
    "Nam hendrerit sapien vitae lorem sagittis, quis hendrerit ex scelerisque.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Nullam tincidunt sem eu turpis efficitur mollis.",
    "Duis nec turpis interdum, dapibus justo non, fringilla lorem.",
    "Praesent feugiat vitae ante eu pharetra.",
    "Mauris malesuada metus ac augue dictum fringilla.",
    "Praesent in metus feugiat, gravida mi ac, sagittis nisl.",
    "Cras vulputate semper sapien, ac faucibus enim volutpat a.",
    (
        "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere"
        " cubilia Curae; Nulla facilisi."
    ),
    (
        "Suspendisse vestibulum, purus eu sollicitus.pytestLorem ipsum dolor sit amet,"
        " consectetur adipiscing elit."
    ),
    (
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium"
        " doloremque laudantium."
    ),
    (
        "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis"
        " praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias"
        " excepturi sint occaecati cupiditate non provident, similique sunt in culpa"
        " qui officia deserunt mollitia animi, id est laborum et dolorum fuga."
    ),
    "Et harum quidem rerum facilis est et expedita distinctio.",
    (
        "Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit"
        " quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda"
        " est, omnis dolor repellendus."
    ),
    (
        "Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus"
        " saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae."
    ),
    (
        "Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis"
        " voluptatibus maiores alias consequatur aut perferendis doloribus asperiores"
        " repellat."
    ),
    (
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore"
        " eu fugiat nulla pariatur."
    ),
    (
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia"
        " deserunt mollit anim id est laborum."
    ),
    (
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium"
        " doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore"
        " veritatis et quasi architecto beatae vitae dicta sunt explicabo."
    ),
    (
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,"
        " sed quia consequuntur magni dolores eos qui ratione voluptatem sequi"
        " nesciunt."
    ),
    (
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur,"
        " adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et"
        " dolore magnam aliquam quaerat voluptatem."
    ),
    (
        "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit"
        " laboriosam, nisi ut aliquid ex ea commodi consequatur."
    ),
    (
        "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam"
        " nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas"
        " nulla pariatur?"
    ),
    (
        "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis"
        " prameris."
    ),
]


@pytest.fixture()
def fake_data() -> str:
    num = random.randint(2, 6)
    fake = [random.choice(data) for _ in range(num)]
    return " ".join(fake)
