import streamlit as st

conn = st.connection('mysql', type='sql')

st.set_page_config(page_title="Earthquake Report", page_icon="🌎", layout="wide")

st.title("Global Seismic Trends: Data-Driven Earthquake Insights")
st.markdown("""
***This application provides real-time earthquake data and reports.***
""")

st.write("1. Top 10 strongest earthquakes (mag)")
query = """SELECT * FROM earthquakes ORDER BY mag DESC LIMIT 10"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("2. Top 10 deepest earthquakes (depth_km)")
query = """SELECT * FROM earthquakes ORDER BY depth_km DESC LIMIT 10"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)
    
st.write("3. Shallow earthquakes < 50 km and mag > 7.5")
query = """SELECT * FROM earthquakes WHERE depth_km < 50 AND mag > 7.5"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("5. Average magnitude per magnitude type (magType)")
query = """SELECT magType, AVG(mag) as avg_magnitude FROM earthquakes GROUP BY magType"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("6. Year with most earthquakes")
query = """SELECT YEAR(time) as Year, COUNT(*) as Earthquake_count FROM earthquakes 
GROUP BY YEAR(time) ORDER BY earthquake_count DESC LIMIT 1"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("7. Month with highest number of earthquakes")
query = """SELECT MONTHNAME(time) as Month, COUNT(*) as Earthquake_count FROM earthquakes 
GROUP BY MONTHNAME(time) ORDER BY earthquake_count DESC LIMIT 1"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("8. Day of week with most earthquakes")
query = """SELECT DAYNAME(time) as Day_of_Week, COUNT(*) as Earthquake_count FROM earthquakes 
GROUP BY DAYNAME(time) ORDER BY earthquake_count DESC LIMIT 1"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("9. Count of earthquakes per hour of day")
query = """SELECT HOUR(time) as Hour_of_Day, COUNT(*) as Earthquake_count FROM earthquakes GROUP BY HOUR(time) ORDER BY Hour_of_Day"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("10. Most active reporting network (net)")
query = """SELECT net as Network, COUNT(*) as Earthquake_count FROM earthquakes 
GROUP BY net ORDER BY earthquake_count DESC LIMIT 1"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("11. Top 5 places with highest casualties")
query = """SELECT place as Place, SUM(casualties) as Total_Casualties FROM earthquakes
GROUP BY place ORDER BY Total_Casualties DESC LIMIT 5"""
st.code(query, language="sql")
# df = conn.query(query, ttl=600)
# st.dataframe(df, use_container_width=True, hide_index=True)
st.write("**Note:** The 'casualties' column is not available in the current dataset. Please ensure that the dataset includes this information for accurate reporting.")

st.write("13. Average economic loss by alert level")
query = """SELECT alert as Alert, AVG(economic_loss) as Average_Economic_Loss FROM earthquakes GROUP BY alert"""
st.code(query, language="sql")
# df = conn.query(query, ttl=600)
# st.dataframe(df, use_container_width=True, hide_index=True)
st.write("**Note:** The 'economic_loss' column is not available in the current dataset. Please ensure that the dataset includes this information for accurate reporting.")


st.write("14. Count of reviewed vs automatic earthquakes (status)")
query = """SELECT status as Status, COUNT(*) as Earthquake_count FROM earthquakes GROUP BY status"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("15. Count by earthquake type (type)")
query = """SELECT type as Type, COUNT(*) as Earthquake_count FROM earthquakes GROUP BY type"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("16. Number of earthquakes by data type (types)")
query = """SELECT types as Types, COUNT(*) as Earthquake_count FROM earthquakes GROUP BY types"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("18. Events with high station coverage (nst > threshold)")
query = """SELECT * FROM earthquakes WHERE nst > 50"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("19. Number of tsunamis triggered per year")  
query = """SELECT YEAR(time) as Year, SUM(tsunami) as Tsunami_count FROM earthquakes GROUP BY YEAR(time) ORDER BY Year"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("20. Count earthquakes by alert levels (red, orange, etc.).")  
query = """SELECT alert as Alert_Level, COUNT(*) as Earthquake_count FROM earthquakes GROUP BY alert"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("21. Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years")  
query = """SELECT place as Place, AVG(mag) as Average_Magnitude FROM earthquakes 
WHERE time >= DATE_SUB(NOW(), INTERVAL 5 YEAR) 
GROUP BY place ORDER BY Average_Magnitude DESC LIMIT 5"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("22. Find countries that have experienced both shallow and deep earthquakes within the same month")  
query = """ 
 SELECT 
    shallow.Country,
    shallow.year as Year,
    shallow.Month,
    shallow.Shallow_Count,
    deep.Deep_count
FROM (
    SELECT 
        place as Country,
        YEAR(time) AS Year,
        MONTHNAME(time) AS Month,
        COUNT(*) AS shallow_Count
    FROM earthquakes
    WHERE depth_km <= 70.0
    GROUP BY Country, YEAR(time), MONTHNAME(time)
) AS shallow
INNER JOIN (
    SELECT 
        place as Country,
        YEAR(time) AS Year,
        MONTHNAME(time) AS Month,
        COUNT(*) AS Deep_Count
    FROM earthquakes
    WHERE depth_km > 300.0
    GROUP BY Country, YEAR(time), MONTHNAME(time)
) AS deep 
ON shallow.Country = deep.Country 
   AND shallow.Year = deep.Year 
   AND shallow.Month = deep.Month
ORDER BY shallow.Year DESC, shallow.Month DESC, shallow.Country ASC"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("23. Compute the year-over-year growth rate in the total number of earthquakes globally.")  
query = """WITH YearlyCounts AS (
    SELECT 
        YEAR(time) AS Year,
        COUNT(*) AS Total
    FROM 
        earthquakes
    GROUP BY 
        YEAR(time)
    ),
    YoYCalculations AS (
        SELECT 
            Year,
            Total,
            LAG(Total, 1) OVER (ORDER BY Year) AS Prev_year
        FROM 
            YearlyCounts
    )
    SELECT 
        Year,
        Total,
        Prev_year,
        CASE 
            WHEN Prev_year IS NULL THEN 0
            WHEN Prev_year = 0 THEN 0
            ELSE ROUND(((Total - Prev_year) / Prev_year) * 100, 2)
        END AS YOY_growth_percentage
    FROM 
        YoYCalculations
    ORDER BY Year"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("24. List the 3 most seismically active regions by combining both frequency and average magnitude.") 
st.write("Didnt understand the question") 
# query = """"""
# st.code(query, language="sql")
# df = conn.query(query, ttl=600)
# st.dataframe(df, use_container_width=True, hide_index=True)

st.write("25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.")  
query = """SELECT 
        place,
        COUNT(*) AS Total,
        ROUND(AVG(depth_km), 2) AS Average
    FROM 
        earthquakes
    WHERE 
        latitude >= -5.0 
        AND latitude <= 5.0
    GROUP BY 
        place
    ORDER BY 
        Average DESC"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("26. Identify countries having the highest ratio of shallow to deep earthquakes.")  
query = """
    WITH earth AS (
        SELECT 
            place,
            COUNT(CASE WHEN depth_km < 70 THEN 1 END) AS shallow,
            COUNT(CASE WHEN depth_km >= 300 THEN 1 END) AS deep,
            COUNT(*) AS total
        FROM 
            earthquakes
        WHERE 
            place IS NOT NULL
            AND depth_km IS NOT NULL
        GROUP BY 
            place
    )
    SELECT 
        place,
        shallow,
        deep,
        total,
        ROUND(shallow / NULLIF(deep, 0), 2) AS shallow_deep_ratio
    FROM 
        earth
    WHERE 
        total >= 10 
    ORDER BY 
        shallow_deep_ratio DESC, 
        shallow DESC;
"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("27. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.")  
query = """
    WITH average AS (
    SELECT 
        AVG(CASE WHEN tsunami = 1 THEN mag END) AS avg_with_tsunami,
        AVG(CASE WHEN tsunami = 0 OR tsunami IS NULL THEN mag END) AS avg_without_tsunami
    FROM 
        earthquakes
    WHERE 
        mag IS NOT NULL
    )
    SELECT 
        ROUND(avg_with_tsunami, 2) AS Average_with_tsunami,
        ROUND(avg_without_tsunami, 2) AS Average_without_tsunami,
        ROUND(ABS(avg_with_tsunami - avg_without_tsunami), 2) AS Mag_Difference
    FROM 
        average
"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)


st.write("28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)")  
query = """
    WITH Errors AS (
    SELECT 
        id, 
        place,
        mag,
        gap,
        rms,
        (gap - AVG(gap) OVER()) / NULLIF(STDDEV(gap) OVER(), 0) AS gap_z,
        (rms - AVG(rms) OVER()) / NULLIF(STDDEV(rms) OVER(), 0) AS rms_z
    FROM 
        earthquakes
    WHERE 
        gap IS NOT NULL 
        AND rms IS NOT NULL
    )
    SELECT 
        id,
        place,
        mag as Mag,
        gap AS Gap,
        rms AS RMS,
        ROUND(gap_z + rms_z, 2) AS error_margin_score
    FROM 
        Errors
    ORDER BY 
        error_margin_score DESC
    LIMIT 10
"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("30. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.")  
query = """
   SELECT 
        place,
        depth_km as Depth_KM,
        COUNT(*) AS deep_earthquake_count,
        ROUND(AVG(depth_km), 1) AS avg_depth_km,
        ROUND(MAX(depth_km), 1) AS max_depth_km,
        ROUND(AVG(mag), 2) AS avg_magnitude
    FROM 
        earthquakes
    WHERE 
        depth_km > 300
        AND place IS NOT NULL
    GROUP BY 
        place,
        Depth_KM
    ORDER BY 
        deep_earthquake_count DESC
"""
st.code(query, language="sql")
df = conn.query(query, ttl=600)
st.dataframe(df, use_container_width=True, hide_index=True)

