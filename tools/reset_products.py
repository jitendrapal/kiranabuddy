import os

from google.cloud import firestore
from google.oauth2 import service_account

# Dummy product data for testing
PRODUCTS = [

{"selling_price":120,"barcode":"11100000001","brand":"Daawat","name":"Daawat Basmati Rice 1kg","normalized_name":"daawat basmati rice 1kg","product_id":"prod-001","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"kg","created_at":"2025-11-16T10:00:00.000000","updated_at":"2025-11-16T10:05:00.000001","batches":{"batch_001":{"expiry_date":"2026-12-31","qty":50,"cost_price":100,"added_on":"2025-11-16T10:00:00.000000"}}},
{"selling_price":95,"barcode":"11100000002","brand":"Tata Sampann","name":"Tata Sampann Toor Dal 1kg","normalized_name":"tata sampann toor dal 1kg","product_id":"prod-002","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"kg","created_at":"2025-11-16T10:10:00.000000","updated_at":"2025-11-16T10:15:00.000002","batches":{"batch_001":{"expiry_date":"2026-11-15","qty":60,"cost_price":80,"added_on":"2025-11-16T10:10:00.000000"}}},
{"selling_price":85,"barcode":"11100000003","brand":"Aashirvaad","name":"Aashirvaad Atta 5kg","normalized_name":"aashirvaad atta 5kg","product_id":"prod-003","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"kg","created_at":"2025-11-16T10:20:00.000000","updated_at":"2025-11-16T10:25:00.000003","batches":{"batch_001":{"expiry_date":"2026-12-01","qty":40,"cost_price":70,"added_on":"2025-11-16T10:20:00.000000"}}},
{"selling_price":60,"barcode":"11100000004","brand":"Amul","name":"Amul Butter 500g","normalized_name":"amul butter 500g","product_id":"prod-004","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"pieces","created_at":"2025-11-16T10:30:00.000000","updated_at":"2025-11-16T10:35:00.000004","batches":{"batch_001":{"expiry_date":"2026-10-15","qty":30,"cost_price":45,"added_on":"2025-11-16T10:30:00.000000"}}},
{"selling_price":78,"barcode":"11100000005","brand":"Nestle","name":"Nestle Maggi 70g","normalized_name":"nestle maggi 70g","product_id":"prod-005","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"pieces","created_at":"2025-11-16T10:40:00.000000","updated_at":"2025-11-16T10:45:00.000005","batches":{"batch_001":{"expiry_date":"2026-09-01","qty":50,"cost_price":65,"added_on":"2025-11-16T10:40:00.000000"}}},
{"selling_price":60,"barcode":"11100000006","brand":"Tata Salt","name":"Tata Salt 1kg","normalized_name":"tata salt 1kg","product_id":"prod-006","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"kg","created_at":"2025-11-16T10:50:00.000000","updated_at":"2025-11-16T10:55:00.000006","batches":{"batch_001":{"expiry_date":"2027-01-22","qty":25,"cost_price":57,"added_on":"2025-11-16T10:50:00.000000"}}},
{"selling_price":50,"barcode":"11100000007","brand":"Amul","name":"Amul Milk 1L","normalized_name":"amul milk 1l","product_id":"prod-007","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"pieces","created_at":"2025-11-16T11:00:00.000000","updated_at":"2025-11-16T11:05:00.000007","batches":{"batch_001":{"expiry_date":"2026-11-25","qty":70,"cost_price":35,"added_on":"2025-11-16T11:00:00.000000"}}},
{"selling_price":60,"barcode":"11100000008","brand":"Parle G","name":"Parle G Biscuits 200g","normalized_name":"parle-g biscuits 200g","product_id":"prod-008","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"pieces","created_at":"2025-11-16T11:10:00.000000","updated_at":"2025-11-16T11:15:00.000008","batches":{"batch_001":{"expiry_date":"2027-06-20","qty":90,"cost_price":20,"added_on":"2025-11-16T11:10:00.000000"}}},
{"selling_price":30,"barcode":"11100000009","brand":"Surf Excel","name":"Surf Excel Detergent 1kg","normalized_name":"surf excel detergent 1kg","product_id":"prod-009","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"kg","created_at":"2025-11-16T11:20:00.000000","updated_at":"2025-11-16T11:25:00.000009","batches":{"batch_001":{"expiry_date":"2027-04-03","qty":12,"cost_price":24,"added_on":"2025-11-16T11:20:00.000000"}}},
{"selling_price":70,"barcode":"11100000010","brand":"Tata Tea","name":"Tata Tea Gold 500g","normalized_name":"tata tea gold 500g","product_id":"prod-010","shop_id":"8e70a29d-acda-423e-a27b-9b9c870616a7","unit":"pieces","created_at":"2025-11-16T11:30:00.000000","updated_at":"2025-11-16T11:35:00.000010","batches":{"batch_001":{"expiry_date":"2027-04-02","qty":127,"cost_price":50,"added_on":"2025-11-16T11:30:00.000000"}}},
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

