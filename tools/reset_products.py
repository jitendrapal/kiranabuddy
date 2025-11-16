import os

from google.cloud import firestore
from google.oauth2 import service_account

# Dummy product data for testing
PRODUCTS = [
{
  "selling_price": 30,
  "barcode": "8901000000001",
  "brand": "Tata Sampann",
  "cost_price": 25,
  "created_at": "2025-11-15T11:09:56.877745",
  "current_stock": 79,
  "expiry_date": "2025-11-15",
  "name": "Tata Sampann Toor Dal 1kg",
  "normalized_name": "tata sampann toor dal 1kg",
  "product_id": "b1420db9-3e6e-4758-89b0-70a89d386f04",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T22:03:05.169941"
},
{
  "selling_price": 40,
  "barcode": "8901000000002",
  "brand": "Aashirvaad",
  "cost_price": 37,
  "created_at": "2025-11-15T11:10:12.123456",
  "current_stock": 1,
  "expiry_date": "2025-11-12",
  "name": "Aashirvaad Atta 5kg",
  "normalized_name": "aashirvaad atta 5kg",
  "product_id": "c1521eb9-4f6f-4820-90b1-81b91d297f55",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-16T14:30:30.563935"
},
   {
  "selling_price": 60,
  "barcode": "8901000000003",
  "brand": "Amul",
  "cost_price": 40,
  "created_at": "2025-11-15T11:12:00.234567",
  "current_stock": 20,
  "expiry_date": "2025-11-01",
  "name": "Amul Butter 500g",
  "normalized_name": "amul butter 500g",
  "product_id": "d1622fc9-5e7f-4931-91c2-92c92e3a8f66",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T11:35:20.987654"
}
,{
  "selling_price": 80,
  "barcode": "8901000000004",
  "brand": "MDH",
  "cost_price": 70,
  "created_at": "2025-11-15T11:13:15.345678",
  "current_stock": 15,
  "expiry_date": "2025-12-01",
  "name": "MDH Turmeric Powder 100g",
  "normalized_name": "mdh turmeric powder 100g",
  "product_id": "e1723gd9-6f8f-5042-92d3-a3d93f4b9g77",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T11:40:30.123456"
}
,
    {
  "selling_price": 78,
  "barcode": "8901000000005",
  "brand": "Nestle",
  "cost_price": 65,
  "created_at": "2025-11-15T11:14:25.456789",
  "current_stock": 65,
  "expiry_date": "2026-01-01",
  "name": "Nestle Maggi 70g",
  "normalized_name": "nestle maggi 70g",
  "product_id": "f1824he9-7g9g-5153-93e4-b4e04g5c0h88",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T23:51:07.549535"
}
,
    {
  "selling_price": 60,
  "barcode": "8901000000006",
  "brand": "Tata Salt",
  "cost_price": 57,
  "created_at": "2025-11-15T11:15:35.567890",
  "current_stock": 25,
  "expiry_date": "2026-01-22",
  "name": "Tata Salt 1kg",
  "normalized_name": "tata salt 1kg",
  "product_id": "g1925if9-8h0h-5264-94f5-c5f15h6d1i99",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T11:50:50.345678"
}
,
    {
  "selling_price": 50,
  "barcode": "8901000000007",
  "brand": "Amul",
  "cost_price": 35,
  "created_at": "2025-11-15T11:16:45.678901",
  "current_stock": 70,
  "expiry_date": "2026-03-24",
  "name": "Amul Milk 1L",
  "normalized_name": "amul milk 1l",
  "product_id": "h2026jg9-9i1i-5375-95g6-d6g26i7e2j10",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T14:50:03.053881"
}
,
    {
  "selling_price": 60,
  "barcode": "8901000000008",
  "brand": "Parle G",
  "cost_price": 20,
  "created_at": "2025-11-15T11:17:55.789012",
  "current_stock": 90,
  "expiry_date": "2026-06-20",
  "name": "Parle g Biscuits 200g",
  "normalized_name": "parle-g biscuits 200g",
  "product_id": "i2127kh9-0j2j-5486-96h7-e7h37j8f3k21",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-15T14:37:35.341491"
}
,
   {
  "selling_price": 30,
  "barcode": "8901000000009",
  "brand": "Surf Excel",
  "cost_price": 24,
  "created_at": "2025-11-15T11:19:05.890123",
  "current_stock": 12,
  "expiry_date": "2026-04-03",
  "name": "Surf Excel Detergent 1kg",
  "normalized_name": "surf excel detergent 1kg",
  "product_id": "j2228li9-1k3k-5597-97i8-f8i48k9g4l32",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated": "2025-11-15T12:05:20.678901"
   },
    {
  "selling_price": 70,
  "barcode": "9789463056915",
  "brand": "Tata Tea",
  "cost_price": 50,
  "created_at": "2025-11-15T11:20:15.901234",
  "current_stock": 127,
  "expiry_date": "2026-04-02",
  "name": "Tata Tea Gold 500g",
  "normalized_name": "tata tea gold 500g",
  "product_id": "k2329mj9-2l4l-5608-98j9-g9j59l0h5m43",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "pieces",
  "updated_at": "2025-11-16T14:30:09.081924"
}
,{
  "selling_price": 120,
  "barcode": "8901000000010",
  "brand": "Daawat",
  "cost_price": 100,
  "created_at": "2025-11-16T15:00:00.000000",
  "current_stock": 50,
  "expiry_date": "2026-12-31",
  "name": "Daawat Basmati Rice",
  "normalized_name": "daawat basmati rice",
  "product_id": "l2430nk9-3m5m-5719-99k0-h0k60m1n6o54",
  "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
  "unit": "kg",
  "updated_at": "2025-11-16T15:05:00.123456"
},
]


def get_firestore_client():
    """Create a Firestore client using the local service-account key.

    Looks for firbasekey.json one level above this tools/ directory.
    """
    key_path = os.path.join(os.path.dirname(__file__), "..", "firbasekey.json")
    credentials = service_account.Credentials.from_service_account_file(key_path)
    project_id = credentials.project_id
    return firestore.Client(credentials=credentials, project=project_id)

SHOP_ID = "8e70a29d-acda-423e-a27b-9b9c870616a7"


def reset_products():
    db = get_firestore_client()
    products_ref = db.collection("products")

    # Delete existing products for this shop
    docs = products_ref.where("shop_id", "==", SHOP_ID).stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1
    print(f"Deleted {deleted} old products for shop {SHOP_ID}")

    # Insert new products
    for p in PRODUCTS:
        product_id = p["product_id"]
        products_ref.document(product_id).set(p)
    print(f"Inserted {len(PRODUCTS)} products for shop {SHOP_ID}")


if __name__ == "__main__":
    reset_products()

