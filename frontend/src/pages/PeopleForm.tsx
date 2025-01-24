import { Button } from "@/components/ui/button";
import { AlertDestructive } from "@/components/ui/AlertDestructive";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/lib/axios";

function DisasterForm(): JSX.Element {
    const [City, setCity] = useState("");
    const [Province, setProvince] = useState("");
    const [disasterType, setdisasterType] = useState("");
    const [disasterDescription, setdisasterDescription] = useState("");
    const [error, setError] = useState<string | null>(null);
    const user_id = localStorage.getItem("user_id")
    const navigate = useNavigate();
  
    const validatePage1 = () => {
      if (!City || !disasterType || !disasterDescription || !Province) {
        setError("Please fill out all fields on this page.");
        return false;
      }
      setError(null);
      return true;
    };
  
    const handleSubmit = async () => {
      if (!validatePage1()) return;
    
      try {
        const response = await api.post("/api/disaster-upload", {
          City,
          Province,
          disasterType,
          disasterDescription,
          user_id
        });
        
        navigate("/home");
        console.log(response);
      } catch (error: any) {
        console.error("Error:", error);
        if (error.response) {
          // Log detailed backend response
          console.error("Response Data:", error.response.data);
          console.error("Status:", error.response.status);
          console.error("Headers:", error.response.headers);
        }
        setError("Failed to submit the form. Please try again.");
      }
    };
    

  
    return (
      <>
        <div className="flex flex-col items-center justify-start w-full mt-20">
          <Card className="lg:w-[600px] p-6 pb-0">
            <div className="flex space-x-3 mb-4 w-full items-center justify-center">
              <div
                className={`h-5 w-5 rounded-full bg-red-500/50`}
              ></div>
            </div>
                <CardHeader>
                    <CardTitle>Enter your concerns for natural disasters!</CardTitle>
                    <CardDescription>
                    Please provide your details below to help us give out warnings
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4">
                    {/* First Name and Last Name */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="flex flex-col gap-1">
                        <Label htmlFor="City">City</Label>
                        <Input
                            id="City"
                            value={City}
                            onChange={(e) => setCity(e.target.value)}
                            maxLength={50}
                            placeholder="Hamilton"
                        />
                        </div>
                        <div className="flex flex-col gap-1">
                        <Label htmlFor="Province">Province</Label>
                        <Input
                            id="Province"
                            value={Province}
                            onChange={(e) => setProvince(e.target.value)}
                            maxLength={50}
                            placeholder="Ontario"
                        />
                        </div>
                    </div>
                    <div className="flex flex-col gap-1">
                        <Label htmlFor="job-type">Disaster Type</Label>
                        <Select value={disasterType} onValueChange={setdisasterType}>
                        <SelectTrigger id="disaster-type">
                            <SelectValue placeholder="Select a disaster type" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="Wildfires">Wildfires</SelectItem>
                            <SelectItem value="Tsunami">Tsunami</SelectItem>
                            <SelectItem value="Earthquake">Earthquake</SelectItem>
                        </SelectContent>
                        </Select>
                    </div>
                    <div className="flex flex-col gap-1">
                        <Label htmlFor="">Describe What You See</Label>
                        <Textarea
                        id="job-description"
                        value={disasterDescription}
                        onChange={(e) => setdisasterDescription(e.target.value)}
                        maxLength={300}
                        placeholder="Briefly describe the event (max 300 characters)."
                        className="resize-none"
                        />
                        <p className="text-right text-sm text-gray-500">
                        {disasterDescription.length}/400
                        </p>
                    </div>
                    </div>
                </CardContent>
  
            <CardFooter className="flex justify-between">
                <Button variant="outline" onClick={handleSubmit}>
                  Submit Information
                </Button>
            </CardFooter>
          </Card>
          {error && <AlertDestructive error={error} />}
        </div>
      </>
    );
  }
  
  export default DisasterForm;
  