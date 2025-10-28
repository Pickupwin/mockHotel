import random

brands = ["品牌1", "品牌2", "品牌3", "品牌4", "品牌5", "品牌6", "品牌7"]
cities = ["地点01", "地点02", "地点03", "地点04", "地点05", "地点06", "地点07", "地点08", "地点09", "地点10"]

def generate_hotels(n=100, output_file="hotels.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(n):
            brand = random.choice(brands)
            city = random.choice(cities)
            name = f"{brand} {city} Hotel #{i+1}"
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            price = random.randint(200, 1500)
            rating = round(random.uniform(3.0, 5.0), 1)
            f.write(f"{brand},{name},{x:.2f},{y:.2f},{price},{rating}\n")
    print(f"✅ Generated {n} hotels to {output_file}")

if __name__ == "__main__":
    generate_hotels(200)
