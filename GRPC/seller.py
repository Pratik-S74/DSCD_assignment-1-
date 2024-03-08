import grpc
import shopping_pb2
import shopping_pb2_grpc

class SellerClient:
    def __init__(self, market_address):
        self.market_channel = grpc.insecure_channel(market_address)
        self.market_stub = shopping_pb2_grpc.MarketStub(self.market_channel)

    def register_seller(self, seller_uuid, seller_address):
        request = shopping_pb2.RegisterSellerRequest(uuid=seller_uuid, address=seller_address)
        response = self.market_stub.RegisterSeller(request)
        print(f"Registration status: {response.status}")

    def sell_item(self, seller_uuid, product_name, category, quantity, description, seller_address, price):
        request = shopping_pb2.SellItemRequest(
            seller_uuid=seller_uuid,
            product_name=product_name,
            category=category,
            quantity=quantity,
            description=description,
            seller_address=seller_address,
            price=price
        )
        response = self.market_stub.SellItem(request)
        print(f"Sell Item status: {response.status}, Item ID: {response.item_id}")

    def update_item(self, seller_uuid, item_id, new_price, new_quantity, seller_address):
        request = shopping_pb2.UpdateItemRequest(
            seller_uuid=seller_uuid,
            item_id=item_id,
            new_price=new_price,
            new_quantity=new_quantity,
            seller_address=seller_address
        )
        response = self.market_stub.UpdateItem(request)
        print(f"Update Item status: {response.status}")

    def delete_item(self, seller_uuid, item_id, seller_address):
        request = shopping_pb2.DeleteItemRequest(
            seller_uuid=seller_uuid,
            item_id=item_id,
            seller_address=seller_address
        )
        response = self.market_stub.DeleteItem(request)
        print(f"Delete Item status: {response.status}")

    def display_seller_items(self, seller_uuid, seller_address):
        request = shopping_pb2.DisplaySellerItemsRequest(
            seller_uuid=seller_uuid,
            seller_address=seller_address
        )
        response = self.market_stub.DisplaySellerItems(request)

        print("Display Seller Items:")
        for item in response.items:
            print(f"Item ID: {item.item_id}, Price: ${item.price}, Name: {item.product_name}, Category: {item.category},")
            print(f"Description: {item.description}, Quantity Remaining: {item.quantity}")
            print(f"Seller: {item.seller_address}, Rating: {item.rating}")

def main():
    market_address = "instance-1:50051"  # Use the known address of the market
    seller_uuid = input("Enter Seller UUID: ")
    seller_address = "instance-3:68"  # Assuming 68 as the port number

    seller_client = SellerClient(market_address)
    print("Registering Seller...")
    seller_client.register_seller(seller_uuid, seller_address)

    print("Selling Item...")
    product_name = input("Enter Product Name: ")
    category = input("Enter Category (ELECTRONICS/FASHION/OTHERS): ")
    quantity = int(input("Enter Quantity: "))
    description = input("Enter Description: ")
    price = float(input("Enter Price: "))

    seller_client.sell_item(seller_uuid, product_name, category, quantity, description, seller_address, price)

    print("Updating Item...")
    item_id = input("Enter Item ID to update: ")
    new_price = float(input("Enter New Price: "))
    new_quantity = int(input("Enter New Quantity: "))
    seller_client.update_item(seller_uuid, item_id, new_price, new_quantity, seller_address)

    print("Deleting Item...")
    item_id_to_delete = input("Enter Item ID to delete: ")
    seller_client.delete_item(seller_uuid, item_id_to_delete, seller_address)

    print("Displaying Seller Items...")
    seller_client.display_seller_items(seller_uuid, seller_address)

if __name__ == "__main__":
    main()
