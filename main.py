import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('bmw.csv')
   
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    
    # 1. Bar Chart: Count of cars by fuel type
    fuel_counts = df['fuelType'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(fuel_counts.index, fuel_counts.values, color=['blue', 'green', 'orange', 'red', 'purple'])
    plt.xlabel('Fuel Type')
    plt.ylabel('Number of Cars')
    plt.title('1. Bar Chart: Cars by Fuel Type')
    plt.tight_layout()
    
    # 2. Pie Chart: Distribution by transmission type
    transmission_counts = df['transmission'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(transmission_counts.values, labels=transmission_counts.index, autopct='%1.1f%%', 
            colors=['skyblue', 'lightgreen', 'salmon'])
    plt.title('2. Pie Chart: Transmission Types')
    plt.tight_layout()
    
    # 3. Line Chart: Average price by year
    avg_price_by_year = df.groupby('year')['price'].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(avg_price_by_year.index, avg_price_by_year.values, marker='o', color='purple', linewidth=2)
    plt.xlabel('Year')
    plt.ylabel('Average Price (£)')
    plt.title('3. Line Chart: Average Price by Year')
    plt.grid(True)
    plt.tight_layout()
    
    # 4. Histogram: Distribution of mileage
    plt.figure(figsize=(10, 6))
    plt.hist(df['mileage'], bins=30, color='teal', edgecolor='black')
    plt.xlabel('Mileage')
    plt.ylabel('Frequency')
    plt.title('4. Histogram: Mileage Distribution')
    plt.tight_layout()
    
    # 5. Scatter Plot: Price vs Mileage
    plt.figure(figsize=(10, 6))
    plt.scatter(df['mileage'], df['price'], alpha=0.5, c='coral', edgecolor='black')
    plt.xlabel('Mileage')
    plt.ylabel('Price (£)')
    plt.title('5. Scatter Plot: Price vs Mileage')
    plt.tight_layout()
    
    
    
    plt.show()


if __name__ == "__main__":    
    main()