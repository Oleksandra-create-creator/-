class Event:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data or {}

    def __str__(self):
        return f"Event({self.name}, {self.data})"


class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name, subscriber):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(subscriber)

    def unsubscribe(self, event_name, subscriber):
        if event_name in self._subscribers:
            self._subscribers[event_name] = [
                s for s in self._subscribers[event_name] if s is not subscriber
            ]

    def publish(self, event):
        for subscriber in self._subscribers.get(event.name, []):
            subscriber.handle(event)


class Subscriber:
    def __init__(self, name):
        self.name = name
        self.received = []

    def handle(self, event):
        self.received.append(event)
        print(f"  [{self.name}] отримав: {event}")


class EmailSubscriber(Subscriber):
    def handle(self, event):
        super().handle(event)
        print(f"    → відправлено email для {self.name}")


class SMSSubscriber(Subscriber):
    def handle(self, event):
        super().handle(event)
        print(f"    → відправлено SMS для {self.name}")


class PushSubscriber(Subscriber):
    def handle(self, event):
        super().handle(event)
        print(f"    → push-сповіщення для {self.name}")


print("=" * 60)
print("ПАТЕРН OBSERVER — система сповіщень")

bus = EventBus()

email_sub = EmailSubscriber("Марія")
sms_sub = SMSSubscriber("Олег")
push_sub = PushSubscriber("Ірина")

bus.subscribe("new_order", email_sub)
bus.subscribe("new_order", sms_sub)
bus.subscribe("new_order", push_sub)
bus.subscribe("low_stock", email_sub)
bus.subscribe("low_stock", push_sub)

print("\n--- Публікація 'new_order' ---")
bus.publish(Event("new_order", {"id": 1001, "amount": 500}))

print("\n--- Публікація 'low_stock' ---")
bus.publish(Event("low_stock", {"item": "Молоко", "qty": 2}))

print("\n--- Відписка SMS від 'new_order' ---")
bus.unsubscribe("new_order", sms_sub)

print("\n--- Публікація 'new_order' після відписки ---")
bus.publish(Event("new_order", {"id": 1002, "amount": 150}))

print("\n--- РОЗШИРЮВАНІСТЬ: новий підписник без зміни коду ---")


class TelegramSubscriber(Subscriber):
    def handle(self, event):
        super().handle(event)
        print(f"    → Telegram для {self.name}")


tg_sub = TelegramSubscriber("Катерина")
bus.subscribe("new_order", tg_sub)

print("\n--- Публікація з новим TelegramSubscriber ---")
bus.publish(Event("new_order", {"id": 1003, "amount": 300}))

print("\n--- Статистика отриманих подій ---")
for sub in [email_sub, sms_sub, push_sub, tg_sub]:
    print(f"  {sub.name}: {len(sub.received)} подій")
