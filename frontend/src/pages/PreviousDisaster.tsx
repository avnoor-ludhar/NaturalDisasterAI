import axios from "axios";
import { useEffect, useState } from "react";

const PreviousDisaster = () => {
  const [weatherData, setWeatherData] = useState<any>([]);
  const [error, setError] = useState("");

  const getDataFromAPI = async () => {
    try {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: "/api/weather/latest/by-lat-lng?lat=12&lng=77", // Use the proxy route
        headers: {
          "x-api-key": "61837fe9130e349c0e9891d3b0646572a1fb576235009295bb5e4b8191c2e15b",
        },
      };

      const { data } = await axios.request(config);
      setWeatherData(data);
    } catch (error) {
      console.error(error);
      setError("Failed to fetch weather data");
    }
  };

  useEffect(() => {
    getDataFromAPI();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full">
        <h1 className="text-2xl font-bold text-center mb-6">Weather Information</h1>
        {error && (
          <div className="bg-red-100 text-red-700 p-4 rounded-lg mb-4">
            {error}
          </div>
        )}
        {weatherData ? (
          <div className="bg-white shadow-lg rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              {weatherData.summary}
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Temperature</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.temperature}Â°F</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Humidity</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.humidity}%</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Wind Speed</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.windSpeed} mph</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Visibility</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.visibility} miles</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">UV Index</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.uvIndex}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Pressure</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.pressure} hPa</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Ozone Levels</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.ozone} DU</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Cloud Cover</p>
                <p className="text-lg font-bold text-gray-800">{weatherData.cloudCover * 100}%</p>
              </div>
            </div>
            <div className="mt-4 text-sm text-gray-500">
              <p>
                <span className="font-bold">Updated At:</span> {new Date(weatherData.updatedAt).toLocaleString()}
              </p>
              <p>
                <span className="font-bold">Timezone:</span> {weatherData.timezone}
              </p>
            </div>
          </div>
        ) : (
          !error && <p className="text-gray-600 text-center">Loading weather data...</p>
        )}
      </div>
    </div>
  );
};

export default PreviousDisaster;