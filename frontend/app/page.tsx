import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
// import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsTrigger } from "@/components/ui/tabs";
import { TabsList } from "@radix-ui/react-tabs";
import { ArrowLeft, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <div className="w-full flex items-center flex-col">
      <Card className="w-3/4 min-h-screen rounded-none">

      <div className="mx-auto p-8 border-b text-center">
        <h1 className="text-3xl font-bold">Interactive Robotics</h1>
        <p className="text-lg font-extralight">GUI for controlling the simulation of a robot</p>
    </div>

    <div className="space-y-4 px-16 text-lg my-2">


    <Tabs defaultValue="object" className="w-full">
      <TabsList className="grid w-full grid-cols-3 bg-muted p-1 w-fit mx-auto">
        <TabsTrigger value="joint">Joint Control</TabsTrigger>
        <TabsTrigger value="arm">Arm Control</TabsTrigger>
        <TabsTrigger value="object">Object Control</TabsTrigger>
      </TabsList>

      <TabsContent value="joint">
        <Card className="py-4 mx-16 px-4">
          
          <CardContent className="space-y-4 w-full">
            
            <div className="flex grid grid-cols-3 space-x-4 w-full text-xl font-semibold text-center">
              <div></div>
              <div>Position</div>
              <div>Move By</div>
            </div>
            
            <Separator/>

            {['Joint 1', 'Joint 2', 'Joint 2','Joint 2','Joint 2','Joint 2','Joint 2','Joint 2',].map((joint, i) => {
             return (
            <div key={i} className="flex grid grid-cols-3 space-x-4 w-full">
              <div className="flex-1/6 text-center">{joint}</div>
              <div><Input placeholder="0 degrees"/></div>
              <div><Input placeholder="0 degrees"/></div>
            </div>
             )})}

          </CardContent>

          <CardFooter className="text-right">
            <Button>Save and Move</Button>
          </CardFooter>
        </Card>
      </TabsContent>

      <TabsContent value="arm" className="h-full">
        <Card className="py-4 mx-16 px-4 h-full">
          
          <CardContent className="space-y-4 w-full">
            
            <div className="flex grid grid-cols-3 space-x-4 w-full text-xl font-semibold text-center">
              <div></div>
              <div>Position</div>
              <div>Move By</div>
            </div>
            
            <Separator/>

            {['X Coord', 'Y Coord', 'Z Coord','Grasp',].map((joint, i) => {
             return (
            <div key={i} className="flex grid grid-cols-3 space-x-4 w-full">
              <div className="flex-1/6 text-center">{joint}</div>
              <div><Input placeholder="0"/></div>
              <div><Input placeholder="0"/></div>
            </div>
             )})}

          </CardContent>

          <CardFooter className="text-right">
            <Button>Save and Move</Button>
          </CardFooter>
        </Card>
      </TabsContent>

      <TabsContent value="object">
      <Card className="py-4 mx-16 px-4">
          
          <CardContent className="space-y-4 w-full">
            
            <div className="flex justify-evenly w-full">
              <div className="flex flex-col w-5/12">
                <div className="text-xl font-semibold my-2 text-center space-y-2">Object</div>
                {
                  [1,2,3].map((object, i) => {
                    return (
                        <div key={i} className="flex-1/6 text-left border my-2 p-2 rounded-lg">{object}</div>
                    )
                  })
                }
              </div>

              <div className="flex flex-col h-full w-1/16 space-y-4 justify-center my-auto">
                <Button><ArrowRight/></Button>
                <Button><ArrowLeft/></Button>
              </div>

              <div className="flex flex-col w-5/12">
                <div className="text-xl font-semibold my-2 text-center space-y-2">Object</div>
                {
                  [1,2,3].map((object, i) => {
                    return (
                        <div key={i} className="flex-1/6 text-left border my-2 p-2 rounded-lg">{object}</div>
                    )
                  })
                }
              </div>

            </div>

          </CardContent>

        </Card>
      </TabsContent>
      
    </Tabs>

    </div>

      </Card>
    </div>

  );
}
