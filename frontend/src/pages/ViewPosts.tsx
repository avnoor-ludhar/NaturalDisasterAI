import { useState, useEffect } from "react";
import api from "@/lib/axios";
import Post from "@/components/Post";


//displays all posts
function DisasterView(): JSX.Element {
    const [posts, setPosts]= useState<any[]>([]);

    const getData = async () => {
        try{
            const {data} = await api.get("/api/disaster-posts");
            setPosts(data.data);
            console.log(data.data)
        }catch(e){
            console.log(e);
        }
    }

    useEffect(() => {
        getData();
    }, [])

    return (
      <>
        <div className="flex flex-row flex-wrap gap-6 justify-center my-10">
            {posts?.map((post, i)=>
                <Post post={post} key={i}/>
            )
            }
        </div>
      </>
    );
  }
  
  export default DisasterView;