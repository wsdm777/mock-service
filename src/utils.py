from datetime import date
from typing import Sequence

from src.database.models import CurrencyRate
from src.schemas import CurrencyXml, ValCursXml


def convert_currencies_to_xml(
    search_date: date, currencies_data: Sequence[CurrencyRate]
):
    valute_xml_list = []
    for item in currencies_data:
        value_str = f"{item.value:.4f}".replace(".", ",")

        number_of_zeros = len(str(item.currency.nominal)) - 1
        target_precision = 4 + number_of_zeros
        vunit_rate_value = item.value / item.currency.nominal
        vunit_rate_str = f"{vunit_rate_value:.{target_precision}f}".replace(".", ",")

        valute_xml_list.append(
            CurrencyXml(
                valute_id=item.currency.valute_id_prefix,
                num_code=item.currency.num_code,
                char_code=item.currency.char_code,
                nominal=item.currency.nominal,
                name=item.currency.name,
                value=value_str,
                vunit_rate=vunit_rate_str,
            )
        )

    valcurs_xml = ValCursXml(
        date_str=search_date.strftime("%d.%m.%Y"),
        name="Foreign Currency Market",
        valutes=valute_xml_list,
    )

    return valcurs_xml.to_xml()
