from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True) # class 'rest_framework.serializers.ListSerializer' - []
# в переменной positions лежит объект сериализатора ProductPositionSerializer. Это т.н. "вложенный сериализатор".
# Этот объект сериализатора представляет из себя список со словарями. В словарях ключи -
# 'id', 'stock', 'product', 'quantity', 'price', - то есть это названия полей, которые перечислены в переменной
# fields в классе ProductPositionSerializer (строка 14).
# Объект сериализатора ProductPositionSerializer "вложен" в переменную positions для того, чтобы наглядно отобразить связь между
# моделями-таблицами Stock и StockProduct в сериализаторе StockSerializer. Это реализовано ниже в классе Meta, в котором
# переменная positions указана в списке полей fields.
    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

# вот так это выглядит в ответе на GET-запрос. В positions лежит список со словарем с данными из таблицы StockProduct
        # {   "id": 1,
        #     "address": "Усть-Курдюмская",
        #     "products": [1],
        #     "positions": [
        #         {   "id": 1,
        #             "stock": 1,
        #             "product": 1,
        #             "quantity": 2,
        #             "price": "100.00"}
        #     ]
        # }


    def create(self, validated_data):  # validated data {'address': 'djn это мой адрес не дом и не улица, мой адрес сегодня такой: www.ленинград-спб.ru3'}

    # Из документации rfm по методу create() для моделей с полями M-to-M:
    #If there are many to many fields present on the instance then they cannot be set until the model is instantiated,
    #in which case the implementation is like so:

    # example_relationship = validated_data.pop('example_relationship')
    # instance = ExampleModel.objects.create(**validated_data)
    # instance.example_relationship = example_relationship
    # return instance

    # The default implementation also does not handle nested relationships.
    # If you want to support writable nested relationships you'll need to write an explicit `.create()` method.
    # Не сработало...

    #     # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions') # переопределяется переменная positions,
        print(positions) # positions [OrderedDict([('product', <Product: Огурец>), ('quantity', 250), ('price', Decimal('120.50'))]), OrderedDict([('product', <Product: Помидор2>), ('quantity', 100), ('price', Decimal('180.00'))])]

    # validated_data - это словарь (dict) с телом (данными) из post-запроса (в самом post-запросе json, кот. сериализатор
    # конвертирует в питоновский словарь).
    # Теперь positions - это не список, а словарь, из которого методом .pop() удаляются данные по ключу 'positions'

    #     # создаем склад по его параметрам
        stock = super().create(validated_data)
        print(stock)  #stock <Stock: djn это мой адрес не дом и не улица, мой адрес сегодня такой: www.ленинград-спб.ru3>
    #     stock = Stock.objects.create(**validated_data)
    #     stock.positions.set()
    #
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)    #работает, но хз почему, надо дебажить
    #
    #     # здесь вам надо заполнить связанные таблицы
    #     # в нашем случае: таблицу StockProduct
    #     # с помощью списка positions
    #
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'quantity': position.get('quantity'),
                    'price': position.get('price')
                }
            )

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
