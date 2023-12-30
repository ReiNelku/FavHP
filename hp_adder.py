from cs50 import SQL

db = SQL("sqlite:///favhp.db")


def main():
    while True:
        # Ask user for headphone manufacturer
        manufacturer_id = get_spec_id("manufacturer")

        # Ask user for headphone model
        model = input("Type the headphone model: ")

        # Ask user for type of connectivity
        connectivity_id = get_spec_id("connectivity")

        # Ask user for type of form factor
        form_factor_id = get_spec_id("form_factor")

        # Ask user about how open the headphone is
        openness_id = get_spec_id("openness")

        # Ask user for type of driver
        driver_id = get_spec_id("driver")

        # Ask user for sensitivity of headphone
        sensitivity = get_value("sensitivity")

        # Ask user for sensitivity unit
        sens_unit_id = get_spec_id("sens_unit")

        # Ask user for headphone impedance
        impedance = get_value("impedance")

        # Ask user for headphone weight
        weight = get_value("weight")

        # Format image filename
        image = f"{model.replace(' ', '_').casefold()}.jpg"

        # Insert headphone in database
        db.execute(
            "INSERT INTO headphones (manufacturer_id, model, connectivity_id, form_factor_id, openness_id, driver_id, sensitivity, sens_unit_id, impedance, weight, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            manufacturer_id,
            model,
            connectivity_id,
            form_factor_id,
            openness_id,
            driver_id,
            sensitivity,
            sens_unit_id,
            impedance,
            weight,
            image,
        )

        # Ask user to continue adding headphones
        if input("Continue?") != "":
            break


def get_spec_id(spec):
    # Get specification from database
    spec_list = db.execute("SELECT * FROM ?", spec)

    # Format specification in case of sensitivity unit
    if spec == "sens_unit":
        spec = "Sensitivity unit"
    else:
        spec = spec.replace("_", " ").capitalize()

    print(f"{spec}:")

    # Print the list of specifications
    for s in spec_list:
        if "name" in s:
            print(f"{s['id']}. {s['name']}")
        elif "unit" in s:
            print(f"{s['id']}. {s['unit']}")
        else:
            print(f"{s['id']}. {s['type']}")

    return get_id(spec, spec_list)


def get_id(spec, id_list):
    # Check if user has inputed a valid specification id
    while True:
        try:
            id = int(input(f"Select the {spec}: "))
        except:
            print()
        else:
            if id > len(id_list):
                continue
            else:
                break

    return id


def get_value(spec):
    # Check if user has inputed a valid specification value
    while True:
        try:
            spec_value = int(input(f"Type the headphone {spec}: "))
        except ValueError:
            continue
        else:
            break

    return spec_value


if __name__ == "__main__":
    main()
