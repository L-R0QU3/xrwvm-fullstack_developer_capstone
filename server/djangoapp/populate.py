from .models import CarMake, CarModel


def initiate():
    # Datos de marcas (CarMake)
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]
    car_make_instances = []
    for data in car_make_data:
        # Evita duplicados: si ya existe la marca, no la crea de nuevo
        obj, created = CarMake.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        car_make_instances.append(obj)

    # Datos de modelos (CarModel)
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023,
         "car_make": "NISSAN", "dealer_id": 1},
        {"name": "Qashqai", "type": "SUV", "year": 2023,
         "car_make": "NISSAN", "dealer_id": 1},
        {"name": "XTRAIL", "type": "SUV", "year": 2023,
         "car_make": "NISSAN", "dealer_id": 1},
        {"name": "A-Class", "type": "SUV", "year": 2023,
         "car_make": "Mercedes", "dealer_id": 2},
        {"name": "C-Class", "type": "SUV", "year": 2023,
         "car_make": "Mercedes", "dealer_id": 2},
        {"name": "E-Class", "type": "SUV", "year": 2023,
         "car_make": "Mercedes", "dealer_id": 2},
        {"name": "A4", "type": "SUV", "year": 2023,
         "car_make": "Audi", "dealer_id": 3},
        {"name": "A5", "type": "SUV", "year": 2023,
         "car_make": "Audi", "dealer_id": 3},
        {"name": "A6", "type": "SUV", "year": 2023,
         "car_make": "Audi", "dealer_id": 3},
        {"name": "Sorrento", "type": "SUV", "year": 2023,
         "car_make": "Kia", "dealer_id": 4},
        {"name": "Carnival", "type": "SUV", "year": 2023,
         "car_make": "Kia", "dealer_id": 4},
        {"name": "Cerato", "type": "Sedan", "year": 2023,
         "car_make": "Kia", "dealer_id": 4},
        {"name": "Corolla", "type": "Sedan", "year": 2023,
         "car_make": "Toyota", "dealer_id": 5},
        {"name": "Camry", "type": "Sedan", "year": 2023,
         "car_make": "Toyota", "dealer_id": 5},
        {"name": "Kluger", "type": "SUV", "year": 2023,
         "car_make": "Toyota", "dealer_id": 5},
    ]
    for data in car_model_data:
        # Obtiene la instancia de CarMake correspondiente
        car_make = CarMake.objects.get(name=data['car_make'])
        # Evita duplicados por nombre, año y marca
        obj, created = CarModel.objects.get_or_create(
            name=data['name'],
            year=data['year'],
            car_make=car_make,
            defaults={
                'type': data['type'],
                'dealer_id': data['dealer_id'],
            }
        )
