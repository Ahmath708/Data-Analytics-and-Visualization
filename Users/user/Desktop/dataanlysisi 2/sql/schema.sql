-- Database Schema for Data Analytics Project
-- SQL Schema and Queries

-- ============================================
-- SCHEMA DEFINITION
-- ============================================

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Email VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Age INT,
    RegistrationDate DATE
);

-- Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10, 2)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    OrderDate DATE,
    Quantity INT,
    Discount DECIMAL(5, 2),
    UnitPrice DECIMAL(10, 2),
    TotalAmount DECIMAL(10, 2),
    ShippingCost DECIMAL(10, 2),
    OrderStatus VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- ============================================
-- DATA QUERIES
-- ============================================

-- 1. Top 10 Customers by Revenue
SELECT c.CustomerID, c.CustomerName, c.City, SUM(o.TotalAmount) AS TotalSpent, COUNT(o.OrderID) AS OrderCount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.CustomerID, c.CustomerName, c.City
ORDER BY TotalSpent DESC
LIMIT 10;

-- 2. Revenue by City (Top 10)
SELECT c.City, COUNT(DISTINCT c.CustomerID) AS CustomerCount, SUM(o.TotalAmount) AS Revenue
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.City
ORDER BY Revenue DESC
LIMIT 10;

-- 3. Revenue by Age Group
SELECT 
    CASE 
        WHEN c.Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN c.Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN c.Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN c.Age BETWEEN 46 AND 55 THEN '46-55'
        WHEN c.Age BETWEEN 56 AND 65 THEN '56-65'
        ELSE '65+'
    END AS AgeGroup,
    COUNT(o.OrderID) AS OrderCount,
    SUM(o.TotalAmount) AS Revenue
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY AgeGroup
ORDER BY Revenue DESC;

-- 4. Category Performance
SELECT p.Category, COUNT(o.OrderID) AS OrderCount, SUM(o.TotalAmount) AS Revenue, SUM(o.Quantity) AS UnitsSold
FROM Products p
JOIN Orders o ON p.ProductID = o.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.Category
ORDER BY Revenue DESC;

-- 5. Top Products by Revenue (Top 15)
SELECT p.ProductID, p.ProductName, p.Category, COUNT(o.OrderID) AS OrderCount, SUM(o.TotalAmount) AS Revenue
FROM Products p
JOIN Orders o ON p.ProductID = o.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.ProductID, p.ProductName, p.Category
ORDER BY Revenue DESC
LIMIT 15;

-- 6. Monthly Sales Trend
SELECT DATE_FORMAT(o.OrderDate, '%Y-%m') AS YearMonth, 
       COUNT(o.OrderID) AS Orders, 
       SUM(o.TotalAmount) AS Revenue,
       SUM(o.Quantity) AS UnitsSold
FROM Orders o
WHERE o.OrderStatus = 'Completed'
GROUP BY YearMonth
ORDER BY YearMonth;

-- 7. Quarterly Sales
SELECT YEAR(o.OrderDate) AS Year, 
       QUARTER(o.OrderDate) AS Quarter,
       COUNT(o.OrderID) AS Orders, 
       SUM(o.TotalAmount) AS Revenue
FROM Orders o
WHERE o.OrderStatus = 'Completed'
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- 8. Daily Sales Pattern
SELECT DAYNAME(o.OrderDate) AS DayOfWeek, 
       COUNT(o.OrderID) AS Orders, 
       SUM(o.TotalAmount) AS Revenue
FROM Orders o
WHERE o.OrderStatus = 'Completed'
GROUP BY DayOfWeek
ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 9. Order Status Distribution
SELECT OrderStatus, COUNT(*) AS Count, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Orders), 2) AS Percentage
FROM Orders
GROUP BY OrderStatus;

-- 10. Statistical Summary
SELECT 
    AVG(TotalAmount) AS AvgOrderValue,
    MIN(TotalAmount) AS MinOrderValue,
    MAX(TotalAmount) AS MaxOrderValue,
    STDDEV(TotalAmount) AS StdDev,
    COUNT(*) AS TotalOrders
FROM Orders
WHERE OrderStatus = 'Completed';

-- 11. Customer Lifetime Value
SELECT c.CustomerID, c.CustomerName, c.City,
       COUNT(o.OrderID) AS TotalOrders,
       SUM(o.TotalAmount) AS LifetimeValue,
       AVG(o.TotalAmount) AS AvgOrderValue,
       DATEDIFF(MAX(o.OrderDate), MIN(o.OrderDate)) AS CustomerTenure
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.CustomerID, c.CustomerName, c.City
HAVING LifetimeValue > 5000
ORDER BY LifetimeValue DESC;

-- 12. Product Pricing Analysis by Category
SELECT Category, 
       MIN(UnitPrice) AS MinPrice, 
       MAX(UnitPrice) AS MaxPrice, 
       AVG(UnitPrice) AS AvgPrice,
       STDDEV(UnitPrice) AS StdDevPrice
FROM Products
GROUP BY Category
ORDER BY AvgPrice DESC;

-- 13. Cancelled Orders Analysis
SELECT c.CustomerID, c.CustomerName, COUNT(o.OrderID) AS CancelledOrders
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Cancelled'
GROUP BY c.CustomerID, c.CustomerName
ORDER BY CancelledOrders DESC
LIMIT 10;

-- 14. Year-over-Year Growth
WITH current_year AS (
    SELECT SUM(TotalAmount) AS Revenue
    FROM Orders
    WHERE OrderStatus = 'Completed' AND YEAR(OrderDate) = 2025
),
previous_year AS (
    SELECT SUM(TotalAmount) AS Revenue
    FROM Orders
    WHERE OrderStatus = 'Completed' AND YEAR(OrderDate) = 2024
)
SELECT 
    (SELECT Revenue FROM current_year) AS Revenue2025,
    (SELECT Revenue FROM previous_year) AS Revenue2024,
    ((SELECT Revenue FROM current_year) - (SELECT Revenue FROM previous_year)) / (SELECT Revenue FROM previous_year) * 100 AS YoYGrowth;

-- 15. Customer Segmentation (RFM Analysis)
SELECT c.CustomerID, c.CustomerName,
       MAX(o.OrderDate) AS LastOrderDate,
       DATEDIFF(CURRENT_DATE(), MAX(o.OrderDate)) AS Recency,
       COUNT(o.OrderID) AS Frequency,
       SUM(o.TotalAmount) AS Monetary
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.CustomerID, c.CustomerName
ORDER BY Recency ASC, Frequency DESC, Monetary DESC;