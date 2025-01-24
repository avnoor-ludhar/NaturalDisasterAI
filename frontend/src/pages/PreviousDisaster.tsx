import axios from "axios";

const PreviousDisaster = () =>{
    const getDataFromAPI = async () => {
        try{
            let config = {
                method: 'get',
                maxBodyLength: Infinity,
                url: 'https://api.ambeedata.com/weather/latest/by-lat-lng?lat=12&lng=77',
                headers: { 
                    'x-api-key': '61837fe9130e349c0e9891d3b0646572a1fb576235009295bb5e4b8191c2e15b'
                }
            };

            const response = await axios.request(config);
            console.log(response);
        }catch(error){
            console.log(error);
        }

    }

    return (
        <div>
            Hello world
        </div>
    )
    
}

export default PreviousDisaster;