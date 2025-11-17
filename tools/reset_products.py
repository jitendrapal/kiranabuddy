import os

from google.cloud import firestore
from google.oauth2 import service_account

# Dummy product data for testing
PRODUCTS = [

  {
    "selling_price": 120,
    "barcode": "111000000001",
    "brand": "Tata",
    "name": "Tata Tea Gold 500g",
    "normalized_name": "tata tea gold 500g",
    "product_id": "prod-001",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:00:00.000000",
    "updated_at": "2025-11-16T10:05:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-06-30",
        "qty": 100,
        "cost_price": 90,
        "added_on": "2025-11-16T10:00:00.000000"
      }
    }
  },
  {
    "selling_price": 55,
    "barcode": "111000000002",
    "brand": "Tata",
    "name": "Tata Salt 1kg",
    "normalized_name": "tata salt 1kg",
    "product_id": "prod-002",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:01:00.000000",
    "updated_at": "2025-11-16T10:06:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-01-01",
        "qty": 200,
        "cost_price": 45,
        "added_on": "2025-11-16T10:01:00.000000"
      }
    }
  },
  {
    "selling_price": 85,
    "barcode": "111000000003",
    "brand": "Aashirvaad",
    "name": "Aashirvaad Atta 5kg",
    "normalized_name": "aashirvaad atta 5kg",
    "product_id": "prod-003",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:02:00.000000",
    "updated_at": "2025-11-16T10:07:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-11-30",
        "qty": 80,
        "cost_price": 70,
        "added_on": "2025-11-16T10:02:00.000000"
      }
    }
  },
  {
    "selling_price": 120,
    "barcode": "111000000004",
    "brand": "Daawat",
    "name": "Daawat Basmati Rice 1kg",
    "normalized_name": "daawat basmati rice 1kg",
    "product_id": "prod-004",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:03:00.000000",
    "updated_at": "2025-11-16T10:08:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-06-30",
        "qty": 50,
        "cost_price": 100,
        "added_on": "2025-11-16T10:03:00.000000"
      }
    }
  },
  {
    "selling_price": 95,
    "barcode": "111000000005",
    "brand": "TRS",
    "name": "TRS Toor Dal 1kg",
    "normalized_name": "trs toor dal 1kg",
    "product_id": "prod-005",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:04:00.000000",
    "updated_at": "2025-11-16T10:09:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-12-31",
        "qty": 60,
        "cost_price": 80,
        "added_on": "2025-11-16T10:04:00.000000"
      }
    }
  },
  {
    "selling_price": 90,
    "barcode": "111000000006",
    "brand": "TRS",
    "name": "TRS Moong Dal Chilka 1kg",
    "normalized_name": "trs moong dal chilka 1kg",
    "product_id": "prod-006",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:05:00.000000",
    "updated_at": "2025-11-16T10:10:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-11-15",
        "qty": 70,
        "cost_price": 75,
        "added_on": "2025-11-16T10:05:00.000000"
      }
    }
  },
  {
    "selling_price": 100,
    "barcode": "111000000007",
    "brand": "TRS",
    "name": "TRS Urad Dal 1kg",
    "normalized_name": "trs urad dal 1kg",
    "product_id": "prod-007",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:06:00.000000",
    "updated_at": "2025-11-16T10:11:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-02-28",
        "qty": 40,
        "cost_price": 85,
        "added_on": "2025-11-16T10:06:00.000000"
      }
    }
  },
  {
    "selling_price": 92,
    "barcode": "111000000008",
    "brand": "Tata Sampann",
    "name": "Tata Sampann Chana Dal 1kg",
    "normalized_name": "tata sampann chana dal 1kg",
    "product_id": "prod-008",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:07:00.000000",
    "updated_at": "2025-11-16T10:12:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-10-30",
        "qty": 55,
        "cost_price": 70,
        "added_on": "2025-11-16T10:07:00.000000"
      }
    }
  },
  {
    "selling_price": 55,
    "barcode": "111000000009",
    "brand": "MDH",
    "name": "MDH Turmeric Powder 100g",
    "normalized_name": "mdh turmeric powder 100g",
    "product_id": "prod-009",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:08:00.000000",
    "updated_at": "2025-11-16T10:13:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-05-15",
        "qty": 120,
        "cost_price": 40,
        "added_on": "2025-11-16T10:08:00.000000"
      }
    }
  },
  {
    "selling_price": 60,
    "barcode": "111000000010",
    "brand": "MDH",
    "name": "MDH Garam Masala 100g",
    "normalized_name": "mdh garam masala 100g",
    "product_id": "prod-010",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:09:00.000000",
    "updated_at": "2025-11-16T10:14:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-09-10",
        "qty": 90,
        "cost_price": 45,
        "added_on": "2025-11-16T10:09:00.000000"
      }
    }
  },
  {
    "selling_price": 50,
    "barcode": "111000000011",
    "brand": "MDH",
    "name": "MDH Coriander Powder 100g",
    "normalized_name": "mdh coriander powder 100g",
    "product_id": "prod-011",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:10:00.000000",
    "updated_at": "2025-11-16T10:15:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-03-01",
        "qty": 110,
        "cost_price": 38,
        "added_on": "2025-11-16T10:10:00.000000"
      }
    }
  },
  {
    "selling_price": 200,
    "barcode": "111000000012",
    "brand": "Amul",
    "name": "Amul Butter 500g",
    "normalized_name": "amul butter 500g",
    "product_id": "prod-012",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:11:00.000000",
    "updated_at": "2025-11-16T10:16:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-12-20",
        "qty": 40,
        "cost_price": 150,
        "added_on": "2025-11-16T10:11:00.000000"
      }
    }
  },
  {
    "selling_price": 55,
    "barcode": "111000000013",
    "brand": "Amul",
    "name": "Amul Milk 1L",
    "normalized_name": "amul milk 1l",
    "product_id": "prod-013",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:12:00.000000",
    "updated_at": "2025-11-16T10:17:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2025-12-05",
        "qty": 70,
        "cost_price": 40,
        "added_on": "2025-11-16T10:12:00.000000"
      }
    }
  },
  {
    "selling_price": 30,
    "barcode": "111000000014",
    "brand": "Nestle",
    "name": "Nestle Maggi 70g",
    "normalized_name": "nestle maggi 70g",
    "product_id": "prod-014",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:13:00.000000",
    "updated_at": "2025-11-16T10:18:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-10-01",
        "qty": 150,
        "cost_price": 22,
        "added_on": "2025-11-16T10:13:00.000000"
      }
    }
  },
  {
    "selling_price": 40,
    "barcode": "111000000015",
    "brand": "Parle",
    "name": "Parle-G Biscuits 200g",
    "normalized_name": "parle-g biscuits 200g",
    "product_id": "prod-015",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:14:00.000000",
    "updated_at": "2025-11-16T10:19:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-03-15",
        "qty": 120,
        "cost_price": 30,
        "added_on": "2025-11-16T10:14:00.000000"
      }
    }
  },
  {
    "selling_price": 90,
    "barcode": "111000000016",
    "brand": "Haldiram",
    "name": "Haldiram’s Aloo Bhujia 200g",
    "normalized_name": "haldiram aloo bhujia 200g",
    "product_id": "prod-016",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:15:00.000000",
    "updated_at": "2025-11-16T10:20:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-05-10",
        "qty": 100,
        "cost_price": 65,
        "added_on": "2025-11-16T10:15:00.000000"
      }
    }
  },
  {
    "selling_price": 150,
    "barcode": "111000000017",
    "brand": "Haldiram",
    "name": "Haldiram’s Soan Papdi 500g",
    "normalized_name": "haldiram soan papdi 500g",
    "product_id": "prod-017",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:16:00.000000",
    "updated_at": "2025-11-16T10:21:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-12-01",
        "qty": 50,
        "cost_price": 120,
        "added_on": "2025-11-16T10:16:00.000000"
      }
    }
  },
  {
    "selling_price": 45,
    "barcode": "111000000018",
    "brand": "Britannia",
    "name": "Britannia Marie Gold 300g",
    "normalized_name": "britannia marie gold 300g",
    "product_id": "prod-018",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:17:00.000000",
    "updated_at": "2025-11-16T10:22:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-07-15",
        "qty": 80,
        "cost_price": 32,
        "added_on": "2025-11-16T10:17:00.000000"
      }
    }
  },
  {
    "selling_price": 95,
    "barcode": "111000000019",
    "brand": "Surf Excel",
    "name": "Surf Excel Detergent 1kg",
    "normalized_name": "surf excel detergent 1kg",
    "product_id": "prod-019",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:18:00.000000",
    "updated_at": "2025-11-16T10:23:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-09-01",
        "qty": 60,
        "cost_price": 70,
        "added_on": "2025-11-16T10:18:00.000000"
      }
    }
  },
  {
    "selling_price": 60,
    "barcode": "111000000020",
    "brand": "Rin",
    "name": "Rin Detergent 500g",
    "normalized_name": "rin detergent 500g",
    "product_id": "prod-020",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:19:00.000000",
    "updated_at": "2025-11-16T10:24:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-01-01",
        "qty": 100,
        "cost_price": 45,
        "added_on": "2025-11-16T10:19:00.000000"
      }
    }
  },
  {
    "selling_price": 98,
    "barcode": "111000000021",
    "brand": "Tata Sampann",
    "name": "Tata Sampann Tur Dal 1kg",
    "normalized_name": "tata sampann tur dal 1kg",
    "product_id": "prod-021",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:20:00.000000",
    "updated_at": "2025-11-16T10:25:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-08-30",
        "qty": 45,
        "cost_price": 75,
        "added_on": "2025-11-16T10:20:00.000000"
      }
    }
  },
  {
    "selling_price": 105,
    "barcode": "111000000022",
    "brand": "Tata Sampann",
    "name": "Tata Sampann Urad Dal 1kg",
    "normalized_name": "tata sampann urad dal 1kg",
    "product_id": "prod-022",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:21:00.000000",
    "updated_at": "2025-11-16T10:26:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-11-15",
        "qty": 50,
        "cost_price": 83,
        "added_on": "2025-11-16T10:21:00.000000"
      }
    }
  },
  {
    "selling_price": 50,
    "barcode": "111000000023",
    "brand": "Aashirvaad",
    "name": "Aashirvaad Salt 1kg",
    "normalized_name": "aashirvaad salt 1kg",
    "product_id": "prod-023",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:22:00.000000",
    "updated_at": "2025-11-16T10:27:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-02-28",
        "qty": 120,
        "cost_price": 40,
        "added_on": "2025-11-16T10:22:00.000000"
      }
    }
  },
  {
    "selling_price": 60,
    "barcode": "111000000024",
    "brand": "Aashirvaad",
    "name": "Aashirvaad Sugar 1kg",
    "normalized_name": "aashirvaad sugar 1kg",
    "product_id": "prod-024",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:23:00.000000",
    "updated_at": "2025-11-16T10:28:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2030-01-01",
        "qty": 70,
        "cost_price": 45,
        "added_on": "2025-11-16T10:23:00.000000"
      }
    }
  },
  {
    "selling_price": 75,
    "barcode": "111000000025",
    "brand": "Patanjali",
    "name": "Patanjali Dant Kanti Toothpaste 200g",
    "normalized_name": "patanjali dant kanti toothpaste 200g",
    "product_id": "prod-025",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:24:00.000000",
    "updated_at": "2025-11-16T10:29:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-09-01",
        "qty": 90,
        "cost_price": 50,
        "added_on": "2025-11-16T10:24:00.000000"
      }
    }
  },
  {
    "selling_price": 55,
    "barcode": "111000000026",
    "brand": "Patanjali",
    "name": "Patanjali Aloe Vera Juice 1L",
    "normalized_name": "patanjali aloe vera juice 1l",
    "product_id": "prod-026",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:25:00.000000",
    "updated_at": "2025-11-16T10:30:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-07-01",
        "qty": 60,
        "cost_price": 40,
        "added_on": "2025-11-16T10:25:00.000000"
      }
    }
  },
  {
    "selling_price": 35,
    "barcode": "111000000027",
    "brand": "Maggi",
    "name": "Maggi Noodles Masala 70g",
    "normalized_name": "maggi noodles masala 70g",
    "product_id": "prod-027",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:26:00.000000",
    "updated_at": "2025-11-16T10:31:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-11-20",
        "qty": 200,
        "cost_price": 25,
        "added_on": "2025-11-16T10:26:00.000000"
      }
    }
  },
  {
    "selling_price": 88,
    "barcode": "111000000028",
    "brand": "Bikano",
    "name": "Bikano Bhujia 200g",
    "normalized_name": "bikano bhujia 200g",
    "product_id": "prod-028",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:27:00.000000",
    "updated_at": "2025-11-16T10:32:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-04-05",
        "qty": 120,
        "cost_price": 60,
        "added_on": "2025-11-16T10:27:00.000000"
      }
    }
  },
  {
    "selling_price": 300,
    "barcode": "111000000029",
    "brand": "Bikano",
    "name": "Bikano Kaju Katli 500g",
    "normalized_name": "bikano kaju katli 500g",
    "product_id": "prod-029",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:28:00.000000",
    "updated_at": "2025-11-16T10:33:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2026-10-30",
        "qty": 30,
        "cost_price": 250,
        "added_on": "2025-11-16T10:28:00.000000"
      }
    }
  },
  {
    "selling_price": 250,
    "barcode": "111000000030",
    "brand": "Pillsbury",
    "name": "Pillsbury Atta 5kg",
    "normalized_name": "pillsbury atta 5kg",
    "product_id": "prod-030",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:29:00.000000",
    "updated_at": "2025-11-16T10:34:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-05-31",
        "qty": 40,
        "cost_price": 180,
        "added_on": "2025-11-16T10:29:00.000000"
      }
    }
  },
  {
    "selling_price": 120,
    "barcode": "111000000031",
    "brand": "Pillsbury",
    "name": "Pillsbury Cake Mix 500g",
    "normalized_name": "pillsbury cake mix 500g",
    "product_id": "prod-031",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:30:00.000000",
    "updated_at": "2025-11-16T10:35:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-09-10",
        "qty": 50,
        "cost_price": 90,
        "added_on": "2025-11-16T10:30:00.000000"
      }
    }
  },
  {
    "selling_price": 150,
    "barcode": "111000000032",
    "brand": "Fortune",
    "name": "Fortune Sunflower Oil 1L",
    "normalized_name": "fortune sunflower oil 1l",
    "product_id": "prod-032",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:31:00.000000",
    "updated_at": "2025-11-16T10:36:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-03-15",
        "qty": 60,
        "cost_price": 120,
        "added_on": "2025-11-16T10:31:00.000000"
      }
    }
  },
  {
    "selling_price": 145,
    "barcode": "111000000033",
    "brand": "Fortune",
    "name": "Fortune Rice Bran Oil 1L",
    "normalized_name": "fortune rice bran oil 1l",
    "product_id": "prod-033",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:32:00.000000",
    "updated_at": "2025-11-16T10:37:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-06-01",
        "qty": 55,
        "cost_price": 110,
        "added_on": "2025-11-16T10:32:00.000000"
      }
    }
  },
  {
    "selling_price": 100,
    "barcode": "111000000034",
    "brand": "Catch",
    "name": "Catch Black Pepper 50g",
    "normalized_name": "catch black pepper 50g",
    "product_id": "prod-034",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:33:00.000000",
    "updated_at": "2025-11-16T10:38:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2029-01-01",
        "qty": 40,
        "cost_price": 70,
        "added_on": "2025-11-16T10:33:00.000000"
      }
    }
  },
  {
    "selling_price": 80,
    "barcode": "111000000035",
    "brand": "Catch",
    "name": "Catch Cumin Seeds 50g",
    "normalized_name": "catch cumin seeds 50g",
    "product_id": "prod-035",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:34:00.000000",
    "updated_at": "2025-11-16T10:39:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2029-02-01",
        "qty": 50,
        "cost_price": 60,
        "added_on": "2025-11-16T10:34:00.000000"
      }
    }
  },
  {
    "selling_price": 55,
    "barcode": "111000000036",
    "brand": "Everest",
    "name": "Everest Turmeric Powder 100g",
    "normalized_name": "everest turmeric powder 100g",
    "product_id": "prod-036",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:35:00.000000",
    "updated_at": "2025-11-16T10:40:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-04-01",
        "qty": 90,
        "cost_price": 38,
        "added_on": "2025-11-16T10:35:00.000000"
      }
    }
  },
  {
    "selling_price": 65,
    "barcode": "111000000037",
    "brand": "Everest",
    "name": "Everest Red Chilli Powder 100g",
    "normalized_name": "everest red chilli powder 100g",
    "product_id": "prod-037",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:36:00.000000",
    "updated_at": "2025-11-16T10:41:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-03-15",
        "qty": 120,
        "cost_price": 45,
        "added_on": "2025-11-16T10:36:00.000000"
      }
    }
  },
  {
    "selling_price": 300,
    "barcode": "111000000038",
    "brand": "Dabur",
    "name": "Dabur Honey 500g",
    "normalized_name": "dabur honey 500g",
    "product_id": "prod-038",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:37:00.000000",
    "updated_at": "2025-11-16T10:42:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2030-12-31",
        "qty": 30,
        "cost_price": 230,
        "added_on": "2025-11-16T10:37:00.000000"
      }
    }
  },
  {
    "selling_price": 450,
    "barcode": "111000000039",
    "brand": "Dabur",
    "name": "Dabur Chyawanprash 500g",
    "normalized_name": "dabur chyawanprash 500g",
    "product_id": "prod-039",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:38:00.000000",
    "updated_at": "2025-11-16T10:43:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-10-01",
        "qty": 25,
        "cost_price": 350,
        "added_on": "2025-11-16T10:38:00.000000"
      }
    }
  },
  {
    "selling_price": 220,
    "barcode": "111000000040",
    "brand": "Patanjali",
    "name": "Patanjali Ghee 1L",
    "normalized_name": "patanjali ghee 1l",
    "product_id": "prod-040",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:39:00.000000",
    "updated_at": "2025-11-16T10:44:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-08-15",
        "qty": 40,
        "cost_price": 180,
        "added_on": "2025-11-16T10:39:00.000000"
      }
    }
  },
  {
    "selling_price": 150,
    "barcode": "111000000041",
    "brand": "Amul",
    "name": "Amul Cheese Slice 200g",
    "normalized_name": "amul cheese slice 200g",
    "product_id": "prod-041",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:40:00.000000",
    "updated_at": "2025-11-16T10:45:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-05-20",
        "qty": 50,
        "cost_price": 120,
        "added_on": "2025-11-16T10:40:00.000000"
      }
    }
  },
  {
    "selling_price": 350,
    "barcode": "111000000042",
    "brand": "Nestle",
    "name": "Nestle Nido Milk Powder 400g",
    "normalized_name": "nestle nido milk powder 400g",
    "product_id": "prod-042",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:41:00.000000",
    "updated_at": "2025-11-16T10:46:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2029-04-01",
        "qty": 40,
        "cost_price": 280,
        "added_on": "2025-11-16T10:41:00.000000"
      }
    }
  },
  {
    "selling_price": 160,
    "barcode": "111000000043",
    "brand": "Saffola",
    "name": "Saffola Gold Oil 1L",
    "normalized_name": "saffola gold oil 1l",
    "product_id": "prod-043",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:42:00.000000",
    "updated_at": "2025-11-16T10:47:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-09-15",
        "qty": 50,
        "cost_price": 130,
        "added_on": "2025-11-16T10:42:00.000000"
      }
    }
  },
  {
    "selling_price": 85,
    "barcode": "111000000044",
    "brand": "Saffola",
    "name": "Saffola Masala Oats 500g",
    "normalized_name": "saffola masala oats 500g",
    "product_id": "prod-044",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "pieces",
    "created_at": "2025-11-16T10:43:00.000000",
    "updated_at": "2025-11-16T10:48:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2027-12-01",
        "qty": 70,
        "cost_price": 65,
        "added_on": "2025-11-16T10:43:00.000000"
      }
    }
  },
  {
    "selling_price": 400,
    "barcode": "111000000045",
    "brand": "Rajdhani",
    "name": "Rajdhani Basmati Rice 5kg",
    "normalized_name": "rajdhani basmati rice 5kg",
    "product_id": "prod-045",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:44:00.000000",
    "updated_at": "2025-11-16T10:49:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2030-01-01",
        "qty": 20,
        "cost_price": 300,
        "added_on": "2025-11-16T10:44:00.000000"
      }
    }
  },
  {
    "selling_price": 130,
    "barcode": "111000000046",
    "brand": "Kohinoor",
    "name": "Kohinoor Basmati Rice 1kg",
    "normalized_name": "kohinoor basmati rice 1kg",
    "product_id": "prod-046",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:45:00.000000",
    "updated_at": "2025-11-16T10:50:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2029-03-15",
        "qty": 50,
        "cost_price": 100,
        "added_on": "2025-11-16T10:45:00.000000"
      }
    }
  },
  {
    "selling_price": 110,
    "barcode": "111000000047",
    "brand": "TRS",
    "name": "TRS Rajma 1kg",
    "normalized_name": "trs rajma 1kg",
    "product_id": "prod-047",
    "shop_id": "8e70a29d-acda-423e-a27b-9b9c870616a7",
    "unit": "kg",
    "created_at": "2025-11-16T10:46:00.000000",
    "updated_at": "2025-11-16T10:51:00.000001",
    "batches": {
      "batch_001": {
        "expiry_date": "2028-08-01",
        "qty": 45,
        "cost_price": 90,
        "added_on": "2025-11-16T10:46:00.000000"
      }
    }
  }
,
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

