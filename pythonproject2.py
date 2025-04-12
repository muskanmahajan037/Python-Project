import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import warnings
warnings.filterwarnings('ignore')
file_path = "C:/Users/MUSKAN/Downloads/hotel_bookings 2.csv"
df = pd.read_csv(file_path)
#Exploratory Data Analysis, Data cleaning, Stastical analysis
df.head()
df.tail()
df.shape
df.info()
df.columns
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], dayfirst=True)
df.info()
df.describe()
df = df[df['adr']<5000]
df.isnull().sum()
df.drop(['company', 'agent'], axis = 1, inplace = True)
df.dropna(inplace = True)

#Data Analysis and Visualizations
cancelled_perc = df['is_canceled'].value_counts(normalize = True)
print(cancelled_perc)
corr_val = df['total_of_special_requests'].corr(df['is_canceled'])
print(f"Correlation between special requests and cancellation: {corr_val:.2f}")
plt.figure(figsize = (5,4))
plt.title('Reservation status count')
plt.bar(['Not canceled', 'Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()


plt.figure(figsize = (8,4))
ax1 = sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'plasma')
legend_labels,_ = ax1. get_legend_handles_labels()
plt.title('Reservation status in different hotels', size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled'])
plt.show()


#Average Daily Rate in City and Resort Hotel
resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)
city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)

resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()
plt.figure(figsize = (20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()
df['arrival_date'] = pd.to_datetime(df['arrival_date_month'] + ' ' + df['arrival_date_year'].astype(str), format='%B %Y')



# Identify which features influence cancellation(Correlation with cancellations)
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True)[['is_canceled']].sort_values('is_canceled', ascending=False), annot=True, cmap='viridis')
plt.title("Correlation with Booking Cancellation")
plt.show()

# Analyze booking volume over time by hotel type(Plot monthly demand trends)
monthly_counts = df.groupby(['arrival_date', 'hotel']).size().unstack().fillna(0)
colors = sns.color_palette("Set2", n_colors=len(monthly_counts.columns))
monthly_counts.plot(kind='bar', stacked=True, figsize=(14,6), color = colors)
plt.title("Monthly Booking Trends by Hotel Type")
plt.ylabel("Number of Bookings")
plt.xlabel("Arrival Date")
plt.tight_layout()
plt.show()

#Study how early bookings affect cancellations and stay duration.
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='lead_time', y='stays_in_week_nights', hue='is_canceled', alpha=0.5)
plt.title("Lead Time vs Stay Duration (Colored by Cancellation)")
plt.show()

#Monthly Reservation Trends and Cancellation Rates
df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'magma')
legend_labels,_ = ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled'])
plt.show()

#Revenue Loss Potential: ADR from Canceled Bookings
plt.figure(figsize=(15,8))
plt.title('ADR per Month (Canceled Bookings Only)', fontsize=30)
sns.barplot(x='month', y='adr',palette="pastel",data=df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.xlabel('Month')
plt.ylabel('Total ADR for Canceled Bookings')
plt.show()

#Top 10 countries with reservation cancelled
cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data['country'].value_counts()[:10]
colors = sns.color_palette("Set3", n_colors=10)  # 10 colors for 10 countries
plt.figure(figsize=(8,8))
plt.title('Top 10 Countries with Reservation Canceled')
plt.pie(top_10_country, autopct='%.2f%%',labels=top_10_country.index, colors=colors)
plt.show()






df['market_segment'].value_counts()
df['market_segment'].value_counts(normalize = True)
cancelled_data['market_segment'].value_counts(normalize = True)

