import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import Indiaa as weather

regions = {
    "North": [
        "GWALIOR, IN", "SRINAGAR, IN", "BAHRAICH, IN", "AMRITSAR, IN", "NEW DELHI, IN", "HISSAR, IN",
        "JABALPUR, IN", "PATIALA, IN", "LUDHIANA, IN", "TEHRI, IN", "BHAGALPUR, IN", "JHANSI, IN",
        "VARANASI, IN", "MUKTESHWAR, IN", "DEHRADUN, IN", "SAGAR, IN", "SHIMLA, IN", "GUNA, IN",
        "AMBALA, IN", "JAMMU, IN", "INDORE, IN", "GORAKHPUR, IN", "LUCKNOW, IN", "BAREILLY, IN",
        "BHOPAL, IN", "CHANDIGARH, IN", "HOSHANGABAD, IN", "SATNA, IN", "ALLAHABAD, IN", "BETUL, IN",
        "DHAR, IN", "SIDHI, IN", "UMARIA, IN", "RATLAM, IN", "KHANDWA, IN", "SEONI, IN", "RAISEN, IN", "PACHMARHI, IN"
    ],
    "South": [
        "KARWAR, IN", "NAGPUR, IN", "BULDANA, IN", "THIRUVANANTHAPURAM, IN", "MANGALORE, IN", "AURANGABAD, IN",
        "ANANTAPUR, IN", "VELLORE, IN", "KAKINADA, IN", "GULBARGA, IN", "NAGAPPATTINAM, IN", "PORT BLAIR, IN",
        "CHENNAI, IN", "KURNOOL, IN", "HARNAI, IN", "NIZAMABAD, IN", "VISHAKHAPATNAM, IN", "NELLORE, IN",
        "BEGUMPET IN", "OZAR, IN", "CHANDRAPUR, IN", "KOLHAPUR, IN", "AMRAOTI, IN", "BANGALORE, IN", "PUNE, IN",
        "SHOLAPUR, IN", "MADURAI, IN", "HONAVAR, IN", "TIRUCHIRAPPALLI, IN", "GADAG, IN", "KOZHIKODE, IN",
        "CHITRADURGA, IN", "GOA, IN", "RAMAGUNDAM, IN", "RAMANATHAPURAM, IN", "KARAIKAL, IN", "VIJAYAWADA, IN",
        "MACHILIPATNAM, IN", "COIMBATORE, IN", "AKOLA, IN", "MAHABALESHWAR, IN", "BELGAUM, IN", "CUDDALORE, IN",
        "PARBHANI, IN", "SALEM, IN", "SANGLI, IN", "YAVATMAL, IN"
    ],
    "East": [
        "JALPAIGURI, IN", "PATNA, IN", "DALTONGANJ, IN", "CHANDBALI, IN", "JHARSUGUDA, IN", "BHUBANESWAR, IN",
        "ENGLISH BAZAR, IN", "SILCHAR, IN", "IMPHAL, IN", "JAGDALPUR, IN", "RANCHI, IN", "PURI, IN", "PENDRA ROAD, IN",
        "TEZPUR, IN", "GAUHATI, IN", "KOLKATA, IN", "AMBIKAPUR, IN", "BHUJ, IN", "NORTH LAKHIMPUR, IN",
        "State of Bihar, IN",
        "JORHAT, IN", "DARJEELING, IN", "BALASORE, IN", "SAMBALPUR, IN", "KAILASHAHAR, IN", "AGARTALA, IN", "GAYA, IN",
        "RAIPUR, IN", "DIBRUGARH, IN", "KOCH BIHAR, IN", "SHILLONG, IN", "RATNAGIRI, IN", "DHUBRI, IN", "KOLKATA, IN",
        "GOPALPUR, IN", "PASIGHAT, IN", "SILIGURI, IN", "CHERRAPUNJI, IN", "NAGOAN, IN"
    ],
    "West": [
        "BHAVNAGAR, IN", "UDAIPUR, IN", "CHURU, IN", "MUMBAI, IN", "JAISALMER, IN", "DEESA, IN", "PORBANDAR, IN",
        "RAJKOT, IN", "BARMER, IN", "DWARKA, IN", "NALIYA, IN", "KOTA, IN", "GANGANAGAR, IN", "GONDIA, IN",
        "JODHPUR, IN",
        "BIKANER, IN", "JAIPUR, IN", "AJMER, IN", "AHMADABAD, IN", "SURAT, IN"
    ]
}


def get_region_message(region):
    if region == "North":
        return "Great choice! Northern India is known for its historical landmarks, vibrant culture, and delicious cuisine."
    elif region == "South":
        return "Great choice! Southern India is famous for its lush landscapes, beautiful beaches, and rich cultural heritage."
    elif region == "East":
        return "Great choice! Eastern India is known for its scenic beauty, diverse wildlife, and ancient temples."
    elif region == "West":
        return "Great choice! Western India is renowned for its sandy beaches, vibrant festivals, and mouth-watering street food."


def temperature_message(avg_temp):
    if avg_temp < 10:
        return "The average temperature is very cold. Bundle up!"
    elif 10 <= avg_temp < 20:
        return "The average temperature is cool. Grab a light jacket."
    elif 20 <= avg_temp < 25:
        return "The average temperature is mild and pleasant."
    elif 25 <= avg_temp < 30:
        return "The average temperature is warm. Enjoy the weather!"
    elif avg_temp >= 30:
        return "The average temperature is hot. Stay hydrated and seek shade."


def precipitation_message(avg_precip):
    if avg_precip == 0:
        return "No precipitation expected. Enjoy a dry day!"
    elif 0 < avg_precip <= 5:
        return "Expect light precipitation. It might drizzle."
    elif 5 < avg_precip <= 10:
        return "Expect moderate precipitation. Carry an umbrella."
    elif avg_precip > 10:
        return "Expect heavy precipitation. Prepare for rain."


def humidity_message(avg_humidity):
    if avg_humidity <= 30:
        return "The average humidity is low. The air might feel dry."
    elif 31 <= avg_humidity <= 60:
        return "The average humidity is moderate. Enjoy the balanced air!"
    elif 61 <= avg_humidity <= 80:
        return "The average humidity is high. It might feel a bit sticky."
    elif avg_humidity > 80:
        return "The average humidity is very high. Expect humid and uncomfortable conditions."


def wind_speed_message(avg_wind_speed):
    if avg_wind_speed <= 1:
        return "The average wind speed is calm. It's a peaceful day."
    elif 1.01 <= avg_wind_speed <= 5:
        return "The average wind speed is moderate. Enjoy the gentle breeze!"
    elif 5.01 <= avg_wind_speed <= 10:
        return "The average wind speed is breezy. Hold onto your hat!"
    elif 10.01 <= avg_wind_speed <= 20:
        return "The average wind speed is windy. Be cautious, especially if outdoors."
    elif avg_wind_speed > 20:
        return "The average wind speed is strong. Secure loose objects and take precautions."


def generate_verdict(avg_temp, avg_precip, avg_humidity, avg_wind_speed):
    verdict = ""

    if avg_temp < 18:
        if avg_precip > 5:
            if avg_humidity > 80:
                if avg_wind_speed <= 1:
                    verdict += "Cold weather with heavy rain, high humidity, and calm winds. Dress warmly and avoid slippery surfaces.\nPreferably choose another time to go."
                else:
                    verdict += "Cold weather with heavy rain, high humidity, and strong winds. Expect difficult travel conditions.\nIt might not be safe to travel. "
            else:
                if avg_wind_speed <= 1:
                    verdict += "Cold weather with heavy rain, low humidity, and calm winds. Dress warmly and avoid slippery surfaces.\nCarry an Extra pair of clothes."
                else:
                    verdict += "Cold weather with heavy rain, low humidity, and strong winds. Expect difficult travel conditions.\nIt might be unsafe to travel."
        else:
            if avg_humidity > 80:
                if avg_wind_speed <= 1:
                    verdict += "Cold weather with no rain, high humidity, and calm winds. Dress warmly and take care of your skin.\nUse Moisturizers and carry Extra warm Clothes."
                else:
                    verdict += "Cold weather with no rain, high humidity, and strong winds. Dress warmly and prepare for windy conditions.\nMake sure to carry heavy woolen clothes."
            else:
                if avg_wind_speed <= 1:
                    verdict += "Cold weather with no rain, low humidity, and calm winds. Dress warmly and enjoy the peaceful weather.\nIt is safe to travel."
                else:
                    verdict += "Cold weather with no rain, low humidity, and strong winds. Dress warmly and prepare for windy conditions.\nWindy Weather might cause trouble in traveling."
    else:
        if avg_precip > 5:
            if avg_humidity > 80:
                if avg_wind_speed <= 1:
                    verdict += "Warm weather with heavy rain, high humidity, and calm winds. Dress lightly but carry an umbrella.\nPlan your trip accordingly."
                else:
                    verdict += "Warm weather with heavy rain, high humidity, and strong winds. Expect difficult travel conditions and take precautions.\nCarry an Umbrella."
            else:
                if avg_wind_speed <= 1:
                    verdict += "Warm weather with heavy rain, low humidity, and calm winds. Dress lightly but carry an umbrella.\nYour Trip can be Safe but take precautions."
                else:
                    verdict += "Warm weather with heavy rain, low humidity, and strong winds. Expect difficult travel conditions and take precautions.\nTravel might be difficult due to rains."
        else:
            if avg_humidity > 80:
                if avg_wind_speed <= 1:
                    verdict += "Warm weather with no rain, high humidity, and calm winds. Dress lightly and stay hydrated.\nYou can safely travel."
                else:
                    verdict += "Warm weather with no rain, high humidity, and strong winds. Dress lightly and prepare for windy conditions.\nTravel might be difficult due to high humidity."
            else:
                if avg_wind_speed <= 1:
                    verdict += "Warm weather with no rain, low humidity, and calm winds. Dress lightly and enjoy the pleasant weather.\nWeather is perfect to travel."
                else:
                    verdict += "Warm weather with no rain, low humidity, and strong winds. Dress lightly and prepare for windy conditions.\nYou can travel without any problem."

    return verdict


class TravelGuideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("India Travel Guide")

        # Set the window size to be larger
        self.root.geometry("1000x700")

        # Load and set the custom icon
        self.set_window_icon("icon.png")

        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.region_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        self.create_widgets()

        # Make the main frame expandable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def set_window_icon(self, icon_path):
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.wm_iconphoto(True, icon_photo)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading icon: {e}")

    def create_widgets(self):
        ttk.Label(self.main_frame, text="Welcome to the India Travel Guide!").grid(row=0, column=0, columnspan=2,
                                                                                   pady=10)

        ttk.Label(self.main_frame, text="Select a region:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.region_combobox = ttk.Combobox(self.main_frame, textvariable=self.region_var, values=list(regions.keys()))
        self.region_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.region_combobox.bind("<<ComboboxSelected>>", self.update_locations)

        ttk.Label(self.main_frame, text="Select a location:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.location_combobox = ttk.Combobox(self.main_frame, textvariable=self.location_var)
        self.location_combobox.grid(row=2, column=1, padx=10, pady=5)

        self.start_date_entry = DateEntry(self.main_frame, textvariable=self.start_date_var, date_pattern='dd-mm-yyyy')
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=5)

        self.end_date_entry = DateEntry(self.main_frame, textvariable=self.end_date_var, date_pattern='dd-mm-yyyy')
        self.end_date_entry.grid(row=4, column=1, padx=10, pady=5)

        self.submit_button = ttk.Button(self.main_frame, text="Get Weather Forecast", command=self.get_weather_forecast)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.output_text = tk.Text(self.main_frame, wrap=tk.WORD, width=85, height=30)
        self.output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Center the widgets
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

        # Load an initial image or a placeholder
        self.photo = None
        self.image_label = ttk.Label(self.main_frame)
        self.image_label.grid(row=0, column=2, rowspan=7, padx=10, pady=10)

    def load_image(self, image_path):
        # Load the image using PIL
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image if necessary
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

    def update_locations(self, event):
        selected_region = self.region_var.get()
        locations = regions[selected_region]
        self.location_combobox.config(values=locations)
        self.location_var.set('')

        # Update the image based on the selected region
        image_map = {
            'North': 'north1.jpg',
            'South': 'south1.jpg',
            'East': 'east1.jpg',
            'West': 'west1.jpg'
        }
        if selected_region in image_map:
            self.load_image(image_map[selected_region])

    def get_weather_forecast(self):
        selected_region = self.region_var.get()
        selected_location = self.location_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()

        if not selected_region or not selected_location or not start_date or not end_date:
            messagebox.showerror("Error", "Please fill all the fields")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"You have selected {selected_location} in {selected_region} India.\n")
        self.output_text.insert(tk.END, get_region_message(selected_region) + "\n")

        weather_forecast = weather.main(selected_location, start_date, end_date)

        if weather_forecast:
            total_temp = 0
            total_precip = 0
            total_humidity = 0
            total_wind_speed = 0
            count = 0

            self.output_text.insert(tk.END, f"\nWeather forecast for {selected_location}:\n")
            for weather_day in weather_forecast:
                self.output_text.insert(tk.END, f"Date: {weather_day['date']}\n")
                self.output_text.insert(tk.END, f"Predicted Temperature: {weather_day['predicted_temp']} °C\n")
                self.output_text.insert(tk.END, f"Predicted Precipitation: {weather_day['predicted_precip']} mm\n")
                self.output_text.insert(tk.END, f"Humidity: {weather_day['humidity']} %\n")
                self.output_text.insert(tk.END, f"Wind Speed: {weather_day['wind_speed']} m/s\n")
                self.output_text.insert(tk.END, f"Description: {weather_day['description']}\n")
                self.output_text.insert(tk.END, "--------------------------------------------------------\n")

                total_temp += weather_day['predicted_temp']
                total_precip += weather_day['predicted_precip']
                total_humidity += weather_day['humidity']
                total_wind_speed += weather_day['wind_speed']
                count += 1

            avg_temp = total_temp / count
            avg_precip = total_precip / count
            avg_humidity = total_humidity / count
            avg_wind_speed = total_wind_speed / count

            temp_msg = temperature_message(avg_temp)
            precip_msg = precipitation_message(avg_precip)
            humidity_msg = humidity_message(avg_humidity)
            wind_speed_msg = wind_speed_message(avg_wind_speed)

            self.output_text.insert(tk.END, "\nTemperature Summary:\n")
            self.output_text.insert(tk.END, f"Average Temperature: {avg_temp:.2f} °C\n")
            self.output_text.insert(tk.END, temp_msg + "\n")

            self.output_text.insert(tk.END, "\nPrecipitation Summary:\n")
            self.output_text.insert(tk.END, f"Average Precipitation: {avg_precip:.2f} mm\n")
            self.output_text.insert(tk.END, precip_msg + "\n")

            self.output_text.insert(tk.END, "\nHumidity Summary:\n")
            self.output_text.insert(tk.END, f"Average Humidity: {avg_humidity:.2f} %\n")
            self.output_text.insert(tk.END, humidity_msg + "\n")

            self.output_text.insert(tk.END, "\nWind Speed Summary:\n")
            self.output_text.insert(tk.END, f"Average Wind Speed: {avg_wind_speed:.2f} m/s\n")
            self.output_text.insert(tk.END, wind_speed_msg + "\n")

            verdict = generate_verdict(avg_temp, avg_precip, avg_humidity, avg_wind_speed)
            self.output_text.insert(tk.END, "\nVerdict:\n")
            self.output_text.insert(tk.END, verdict + "\n")
        else:
            self.output_text.insert(tk.END, "Weather forecast data not available.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelGuideApp(root)
    root.mainloop()
