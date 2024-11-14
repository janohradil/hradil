
def individual_serial(odpoved) -> dict:
    return {
        "id": str(odpoved.get("_id")),
        "meno": odpoved.get("meno"),
        "priezvisko": odpoved.get("priezvisko"),
        "telefon": odpoved.get("telefon"),
        "sprava": odpoved.get("sprava")
    }


def list_serial(odpoved) -> list:
    return [individual_serial(odpoved) for odpoved in odpoved]

