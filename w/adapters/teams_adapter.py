from pymsteams import connectorcard, cardsection


def send(config, _, **kwargs):
    client = connectorcard(hookurl=config["webhook_url"])
    try:
        card = cardsection()
        card.title(f"You have a new alert for {kwargs.get('alert_type')}")
        card.addFact("Message", f"{kwargs.get('message')}")
        card.addFact("when", f"{kwargs.get('when')}")

        client.color("red")
        client.addSection(card)
        client.send()
    except Exception as e:
        print(e)
