from datetime import datetime

# Yacht class
class Yacht:
    def __init__(self, yacht_id, name, price_per_night, max_guests):
        self.yacht_id = yacht_id
        self.name = name
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.bookings = []

    def is_available(self, start_date, end_date):
        for booking in self.bookings:
            if start_date < booking['end_date'] and end_date > booking['start_date']:
                return False
        return True

    def book(self, customer_name, guests, start_date, end_date):
        if guests > self.max_guests:
            return f"Cannot book. Maximum guests allowed: {self.max_guests}."
        if not self.is_available(start_date, end_date):
            return "Yacht is not available for the selected dates."

        # Calculate cost with discount and tax
        nights = (end_date - start_date).days
        discount = 0.1 if nights > 7 else 0  # 10% discount for bookings > 7 nights
        tax_rate = 0.15  # 15% tax
        subtotal = nights * self.price_per_night
        discount_amount = subtotal * discount
        tax = (subtotal - discount_amount) * tax_rate
        total_cost = subtotal - discount_amount + tax

        # Add booking
        self.bookings.append({
            'customer_name': customer_name,
            'guests': guests,
            'start_date': start_date,
            'end_date': end_date,
            'total_cost': total_cost
        })
        return f"Booking successful! Total cost (after discount and tax): RM{total_cost:.2f}"

    def update_booking(self, customer_name, new_start_date, new_end_date):
        for booking in self.bookings:
            if booking['customer_name'] == customer_name:
                if not self.is_available(new_start_date, new_end_date):
                    return "Yacht is not available for the new dates."
                booking['start_date'] = new_start_date
                booking['end_date'] = new_end_date
                return "Booking updated successfully."
        return "Booking not found."

    def delete_booking(self, customer_name):
        for booking in self.bookings:
            if booking['customer_name'] == customer_name:
                self.bookings.remove(booking)
                return "Booking deleted successfully."
        return "Booking not found."


# Yacht inventory
yachts = [
    Yacht(1, "Luxury Escape", 500, 6),
    Yacht(2, "Sea Breeze", 300, 4),
    Yacht(3, "Ocean Star", 400, 5),
    Yacht(4, "Golden Horizon", 600, 8),
    Yacht(5, "Paradise Pearl", 700, 10)
]

# Function to display available yachts
def display_yachts():
    print("\nAvailable Yachts:")
    for yacht in yachts:
        print(f"ID: {yacht.yacht_id}, Name: {yacht.name}, Price: RM{yacht.price_per_night}/night, Max Guests: {yacht.max_guests}")

# Function to calculate total revenue
def calculate_total_revenue():
    total_revenue = 0
    for yacht in yachts:
        for booking in yacht.bookings:
            total_revenue += booking['total_cost']
    print(f"Total Revenue: RM{total_revenue:.2f}")

# Function to calculate average booking duration
def calculate_average_duration():
    total_nights = 0
    total_bookings = 0
    for yacht in yachts:
        for booking in yacht.bookings:
            total_nights += (booking['end_date'] - booking['start_date']).days
            total_bookings += 1
    if total_bookings == 0:
        print("No bookings to calculate the average duration.")
        return
    average_duration = total_nights / total_bookings
    print(f"Average Booking Duration: {average_duration:.2f} nights")

# Main reservation flow
def reserve_yacht():
    display_yachts()
    try:
        yacht_id = int(input("\nEnter Yacht ID to book: "))
        yacht = next((y for y in yachts if y.yacht_id == yacht_id), None)
        if not yacht:
            print("Invalid Yacht ID.")
            return

        customer_name = input("Enter your name: ")
        guests = int(input("Number of guests: "))
        start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d")
        end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d")

        if end_date <= start_date:
            print("End date must be after start date.")
            return

        result = yacht.book(customer_name, guests, start_date, end_date)
        print(result)
    except ValueError:
        print("Invalid input. Please try again.")

# Update a booking
def update_booking():
    try:
        yacht_id = int(input("Enter Yacht ID for the booking to update: "))
        yacht = next((y for y in yachts if y.yacht_id == yacht_id), None)
        if not yacht:
            print("Invalid Yacht ID.")
            return

        customer_name = input("Enter the customer name for the booking to update: ")
        new_start_date = datetime.strptime(input("Enter new start date (YYYY-MM-DD): "), "%Y-%m-%d")
        new_end_date = datetime.strptime(input("Enter new end date (YYYY-MM-DD): "), "%Y-%m-%d")

        result = yacht.update_booking(customer_name, new_start_date, new_end_date)
        print(result)
    except ValueError:
        print("Invalid input. Please try again.")

# Delete a booking
def delete_booking():
    try:
        yacht_id = int(input("Enter Yacht ID for the booking to delete: "))
        yacht = next((y for y in yachts if y.yacht_id == yacht_id), None)
        if not yacht:
            print("Invalid Yacht ID.")
            return

        customer_name = input("Enter the customer name for the booking to delete: ")
        result = yacht.delete_booking(customer_name)
        print(result)
    except ValueError:
        print("Invalid input. Please try again.")

# Run the program
if __name__ == "__main__":
    while True:
        print("\n--- Yacht Hotel Reservation System ---")
        print("1. View Yachts")
        print("2. Reserve Yacht")
        print("3. Update Booking")
        print("4. Delete Booking")
        print("5. View Total Revenue")
        print("6. View Average Booking Duration")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            display_yachts()
        elif choice == "2":
            reserve_yacht()
        elif choice == "3":
            update_booking()
        elif choice == "4":
            delete_booking()
        elif choice == "5":
            calculate_total_revenue()
        elif choice == "6":
            calculate_average_duration()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")