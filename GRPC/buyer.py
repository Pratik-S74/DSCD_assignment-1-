import grpc
import shopping_pb2
import shopping_pb2_grpc

class BuyerClient:
    def __init__(self, market_address):
        self.market_channel = grpc.insecure_channel(market_address)
        self.market_stub = shopping_pb2_grpc.MarketStub(self.market_channel)

    def search_item(self, item_name="", category="ANY"):
        request = shopping_pb2.SearchItemRequest(item_name=item_name, category=category)
        response = self.market_stub.SearchItem(request)

        print("Searching for Items:")
        for item in response.items:
            print(f"\nItem ID: {item.item_id}")
            print(f"Price: ${item.price}")
            print(f"Name: {item.product_name}")
            print(f"Category: {item.category}")
            print(f"Description: {item.description}")
            print(f"Quantity Remaining: {item.quantity}")
            print(f"Rating: {item.rating} / 5  |  Seller: {item.seller_address}")

    def buy_item(self, item_id, quantity, buyer_address):
        request = shopping_pb2.BuyItemRequest(item_id=item_id, quantity=quantity, buyer_address=buyer_address)
        response = self.market_stub.BuyItem(request)
        print(f"Buy Item status: {response.status}")

    def add_to_wish_list(self, item_id, buyer_address):
        request = shopping_pb2.AddToWishListRequest(item_id=item_id, buyer_address=buyer_address)
        response = self.market_stub.AddToWishList(request)
        print(f"Add to Wish List status: {response.status}")

    def rate_item(self, item_id, buyer_address, rating):
        request = shopping_pb2.RateItemRequest(item_id=item_id, buyer_address=buyer_address, rating=rating)
        response = self.market_stub.RateItem(request)
        print(f"Rate Item status: {response.status}")

def main():
    market_address = "localhost:50051"  # Replace with the actual market address
    buyer_address = "localhost:12346"  # Replace with the actual buyer address

    buyer_client = BuyerClient(market_address)

    print("Searching for Items...")
    buyer_client.search_item()

    print("Buying Item...")
    item_id_to_buy = input("Enter Item ID to Buy: ")
    quantity_to_buy = int(input("Enter Quantity to Buy: "))
    buyer_client.buy_item(item_id_to_buy, quantity_to_buy, buyer_address)

    print("Adding to Wish List...")
    item_id_to_wishlist = input("Enter Item ID to Add to Wish List: ")
    buyer_client.add_to_wish_list(item_id_to_wishlist, buyer_address)

    print("Rating Item...")
    item_id_to_rate = input("Enter Item ID to Rate: ")
    rating_value = int(input("Enter Rating (1-5): "))
    buyer_client.rate_item(item_id_to_rate, buyer_address, rating_value)

if __name__ == "__main__":
    main()
