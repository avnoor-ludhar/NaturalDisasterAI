import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { NavigateFunction, useNavigate } from "react-router-dom";

//Basic homepage using ChadCN UI to ensure ability to navigate to different pages
function HomePage() {
  const navigate: NavigateFunction = useNavigate();

  const handleDisasterUpload = () => {
    navigate('/disaster-form');
  }
  
  const handleDisasterView = () => {
    navigate('/disaster-view');
  }

  return (
    <div className="text-black p-8">
      <h1 className="text-3xl font-semibold text-center bg-gradient-to-r from-red-500 via-red-600 to-red-700 text-transparent bg-clip-text mb-8">
        Welcome to NaturalDisasterAI
      </h1>
      <div className="flex flex-row flex-wrap mb-4 gap-10 justify-evenly">
        <Card className="hover:shadow-lg transition-shadow flex flex-col h-[300px] max-w-[300px]">
          <CardHeader>
            <CardTitle>Upload Data</CardTitle>
            <CardDescription>For disaster prevention</CardDescription>
          </CardHeader>
          <CardContent className="flex-grow">
            <p>Upload data to help others see data from your region for natural disasters</p>
          </CardContent>
          <CardFooter className="mt-auto">
            <Button className="w-full py-3 text-black rounded-lg hover:bg-red-400 bg-red-600" onClick={handleDisasterUpload}>Upload Data</Button>
          </CardFooter>
        </Card>

        <Card className="hover:shadow-lg transition-shadow flex flex-col h-[300px] max-w-[300px]">
          <CardHeader>
            <CardTitle>View Previous Data</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <p>Click here to see if anyone uploaded a disaster near you</p>
          </CardContent>
          <CardFooter className="mt-auto">
            <Button className="w-full py-3 text-black rounded-lg hover:bg-red-400 bg-red-600" onClick={handleDisasterView}>View Data</Button>
          </CardFooter>
        </Card>

        <Card className="hover:shadow-lg transition-shadow flex flex-col h-[300px] max-w-[300px]">
          <CardHeader>
            <CardTitle>View Previous Disasters</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <p>Click here to see history of natural disasters</p>
          </CardContent>
          <CardFooter className="mt-auto">
            <Button className="w-full py-3 text-black rounded-lg hover:bg-red-400 bg-red-600" onClick={() => navigate("/prev-data")}>View Previous Disasters</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default HomePage;
