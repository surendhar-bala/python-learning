from sqlalchemy import Column, Integer, String, Numeric, Date
from .database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    account_code = Column(String, nullable=False)

    scrip_id = Column(String, nullable=False)
    scrip_name = Column(String, nullable=False)
    isin_code = Column(String, nullable=False)

    trade_type = Column(String, nullable=False)
    trade_number = Column(String, nullable=False)

    trade_on = Column(Date, nullable=False)
    credit_date = Column(Date, nullable=False)

    rate = Column(Numeric(18, 2), nullable=False)
    quantity = Column(Numeric(18, 3), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)
    net_amount = Column(Numeric(18, 2), nullable=False)

    stamp_duty_amount = Column(Numeric(18, 2), nullable=False)
    stt = Column(Numeric(18, 2), nullable=False)