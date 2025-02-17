import enum


class CurrencyEnum(enum.Enum):
    USD = "USD"
    RUB = "RUB"
    BYN = "BYN"
    EUR = "EUR"


class OwnerTypeEnum(enum.Enum):
    user = "user"
    group = "group"


class IncomeCategoryEnum(enum.Enum):
    inheritance = "inheritance"
    insurance = "insurance"
    lottery = "lottery"
    pension = "pension"
    present = "present"
    rent = "rent"
    salary = "salary"
    sold_property = "sold property"


class ExpenseCategoryEnum(enum.Enum):
    car = "car"
    clothes = "clothes"
    entertainment = "entertainment"
    food = "food"
    footwear = "footwear"
    furniture = "furniture"
    househoold_goods = "household goods"
    medicine = "medicine"
    regular_payments = "regular payments"
    services = "services"
    transport = "transport"
    utilities = "utilities"
