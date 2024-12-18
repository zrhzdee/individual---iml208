import tkinter as tk
from tkinter import ttk, messagebox
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

        nights = (end_date - start_date).days
        discount = 0.1 if nights > 7 else 0
        tax_rate = 0.15
        subtotal = nights * self.price_per_night
        discount_amount = subtotal * discount
        tax = (subtotal - discount_amount) * tax_rate
        total_cost = subtotal - discount_amount + tax

        self.bookings.append({
            'customer_name': customer_name,
            'guests': guests,
            'start_date': start_date,
            'end_date': end_date,
            'total_cost': total_cost
        })
        return f"Booking successful! Total cost (after discount and tax): RM{total_cost:.2f}"

    def delete_booking(self, customer_name):
        for booking in self.bookings:
            if booking['customer_name'] == customer_name:
                self.bookings.remove(booking)
                return "Booking deleted successfully."
        return "Booking not found."


# Yacht inventory with two additional yachts
yachts = [
    Yacht(1, "Luxury Escape", 500, 6),
    Yacht(2, "Sea Breeze", 300, 4),
    Yacht(3, "Ocean Star", 400, 5),
    Yacht(4, "Golden Horizon", 600, 8),
    Yacht(5, "Paradise Pearl", 700, 10)
]

# GUI Application
class YachtReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yacht Hotel Reservation System")

        self.selected_yacht = tk.StringVar()
        self.customer_name = tk.StringVar()
        self.guests = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Yacht Hotel Reservation", font=("Arial", 18, "bold")).pack(pady=10)

        # Yacht selection
        tk.Label(self.root, text="Select Yacht:").pack()
        yacht_names = [f"{y.yacht_id}: {y.name} (RM{y.price_per_night}/night, Max Guests: {y.max_guests})" for y in yachts]
        self.yacht_combo = ttk.Combobox(self.root, values=yacht_names, textvariable=self.selected_yacht, state="readonly")
        self.yacht_combo.pack(pady=5)

        # Customer details
        tk.Label(self.root, text="Customer Name:").pack()
        tk.Entry(self.root, textvariable=self.customer_name).pack(pady=5)

        tk.Label(self.root, text="Number of Guests:").pack()
        tk.Entry(self.root, textvariable=self.guests).pack(pady=5)

        tk.Label(self.root, text="Start Date (YYYY-MM-DD):").pack()
        tk.Entry(self.root, textvariable=self.start_date).pack(pady=5)

        tk.Label(self.root, text="End Date (YYYY-MM-DD):").pack()
        tk.Entry(self.root, textvariable=self.end_date).pack(pady=5)

        # Buttons
        tk.Button(self.root, text="Reserve Yacht", command=self.reserve_yacht).pack(pady=10)
        tk.Button(self.root, text="Delete Booking", command=self.delete_booking).pack(pady=5)
        tk.Button(self.root, text="View Total Revenue", command=self.view_total_revenue).pack(pady=5)
        tk.Button(self.root, text="View Average Booking Duration", command=self.view_average_duration).pack(pady=5)

    def reserve_yacht(self):
        try:
            yacht_index = int(self.selected_yacht.get().split(":")[0]) - 1
            yacht = yachts[yacht_index]

            name = self.customer_name.get()
            guests = int(self.guests.get())
            start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d")

            if end_date <= start_date:
                messagebox.showerror("Error", "End date must be after start date.")
                return

            result = yacht.book(name, guests, start_date, end_date)
            messagebox.showinfo("Reservation", result)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid input or yacht selection.")

    def delete_booking(self):
        try:
            yacht_index = int(self.selected_yacht.get().split(":")[0]) - 1
            yacht = yachts[yacht_index]

            name = self.customer_name.get()
            if not name:
                messagebox.showerror("Error", "Please enter the customer name.")
                return

            result = yacht.delete_booking(name)
            if "successfully" in result:
                messagebox.showinfo("Delete Booking", result)
            else:
                messagebox.showerror("Delete Booking", result)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid input or yacht selection.")

    def view_total_revenue(self):
        total_revenue = sum(booking['total_cost'] for yacht in yachts for booking in yacht.bookings)
        messagebox.showinfo("Total Revenue", f"Total Revenue: RM{total_revenue:.2f}")

    def view_average_duration(self):
        total_nights = sum((b['end_date'] - b['start_date']).days for yacht in yachts for b in yacht.bookings)
        total_bookings = sum(len(yacht.bookings) for yacht in yachts)
        if total_bookings == 0:
            messagebox.showinfo("Average Booking Duration", "No bookings available to calculate.")
        else:
            avg_duration = total_nights / total_bookings
            messagebox.showinfo("Average Booking Duration", f"Average Duration: {avg_duration:.2f} nights")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = YachtReservationApp(root)
    root.mainloop()
