import enum


class CurrencyEnum(enum.Enum):
    USD = "USD"
    RUB = "RUB"
    BYN = "BYN"
    EUR = "EUR"


class IncomeCategoryEnum(enum.Enum):
    inheritance = "Inheritance"
    insurance = "Insurance"
    lottery = "Lottery"
    pension = "Pension"
    present = "Present"
    rent = "Rent"
    salary = "Salary"
    sold_property = "Sold property"


class ExpenseCategoryEnum(enum.Enum):
    car = "Car"
    clothes = "Clothes"
    entertainment = "Entertainment"
    food = "food"
    footwear = "Footwear"
    furniture = "Furniture"
    househoold_goods = "Household goods"
    medicine = "Medicine"
    regular_payments = "Regular payments"
    services = "Services"
    transport = "Transport"
    utilities = "Utilities"
