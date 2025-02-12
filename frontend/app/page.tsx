"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
// import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsTrigger } from "@/components/ui/tabs";
import { TabsList } from "@radix-ui/react-tabs";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useState } from "react";

export default function Home() {

  const stackingObjects = ['Cube', 'Sphere', 'Prism']

  const [jointPosOriginal, setJointPosOriginal] = useState([0,0,0,0,0,0,0,0]);
  const [jointPosNew, setJointPosNew] = useState([0,0,0,0,0,0,0,0]);
  const [armCoordsOriginal, setArmCoordsOriginal] = useState([0,0,0,0]);
  const [armCoordsNew, setArmCoordsNew] = useState([0,0,0,0]);
  const [objectActive, setObjectActive] = useState<number | undefined>();
  const [isStackActive, setIsStackActive] = useState<number | undefined>();
  const [stack, setStack] = useState<string[]>([]);

  function addToStack(){

    if (objectActive != undefined && stack.length < 5){
      setStack([...stack, String(stackingObjects[objectActive])]);
    }
    setObjectActive(undefined);

  }

  function removeFromStack(){
    if (isStackActive != undefined){
      setStack(stack.filter((_, i) => i != isStackActive));
    }
    setIsStackActive(undefined);
  }


  return (
    <div className="w-full flex items-center flex-col h-full">
    <Card className="w-3/4 h-screen rounded-none">

      <div className="mx-auto p-8 border-b text-center">
        <h1 className="text-3xl font-bold">Interactive Robotics</h1>
        <p className="text-lg font-extralight">GUI for controlling the simulation of a robot</p>
      </div>

      <div className="space-y-4 px-16 text-lg my-2">

        <Tabs defaultValue="joint" className="w-full h-[75vh]">

          <TabsList className="grid grid-cols-3 bg-muted p-1 w-fit mx-auto">
            <TabsTrigger value="joint">Joint Control</TabsTrigger>
            <TabsTrigger value="arm">Arm Control</TabsTrigger>
            <TabsTrigger value="object">Object Control</TabsTrigger>
          </TabsList>

          <Card className="py-4 mx-16 px-4 h-full">

            <TabsContent value="joint">
              
              <CardContent className="space-y-4 w-full">
                
                <div className="flex grid grid-cols-3 space-x-4 w-full text-xl font-semibold text-center">
                  <div></div>
                  <div>Position</div>
                  <div>Move By</div>
                </div>
                
                <Separator/>

                {['Joint 1', 'Joint 2', 'Joint 2','Joint 2','Joint 2','Joint 2','Joint 2','Joint 2',].map((joint, i) => {
                return (
                <div key={i} className="flex grid grid-cols-3 space-x-4 w-full ">
                  <div className="text-center text-base h-full align-middle flex flex-col justify-center">{joint}</div>
                  <div> 
                    <Input type='number' value={ jointPosNew[i] } onChange={(e) => setJointPosNew(jointPosNew.map((v, j) => {
                    if (j == i){
                      return e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                  <div>
                  <Input type='number' value={jointPosNew[i] - jointPosOriginal[i]} onChange={(e) => setJointPosNew(jointPosNew.map((v, j) => {
                    if (j == i){
                      return jointPosOriginal[j] + e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                </div>
                )})}

              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button>Save and Move</Button>
              </CardFooter>
            </TabsContent>

          <TabsContent value="arm" className="h-full">
              
              <CardContent className="w-full space-y-4">
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
                  <div>
                  <Input type='number' value={ armCoordsNew[i] } onChange={(e) => setArmCoordsNew(armCoordsNew.map((v, j) => {
                    if (j == i){
                      return e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                  <div>
                  <Input type='number' value={armCoordsNew[i] - armCoordsOriginal[i]} onChange={(e) => setArmCoordsNew(armCoordsNew.map((v, j) => {
                    if (j == i){
                      return armCoordsOriginal[j] + e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                </div>

                )})}
              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button>Save and Move</Button>
              </CardFooter>

          </TabsContent>

          <TabsContent value="object">
              
              <CardContent className="space-y-4 w-full">
                
                <div className="flex justify-evenly w-full h-[50vh]">
                  <div className="flex flex-col w-5/12">
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Object</div>
                    {
                      stackingObjects.map((object, i) => {
                        return (
                            <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(objectActive==i) && 'bg-blue-200'}`} onClick={()=>setObjectActive(i)}>{object}</div>
                        )
                      })
                    }
                  </div>

                  <div className="flex flex-col h-full w-1/16 space-y-4 justify-center my-auto">
                    <Button onClick={addToStack}><ArrowRight/></Button>
                    <Button onClick={removeFromStack}><ArrowLeft/></Button>
                  </div>

                  <div className="flex flex-col w-5/12">
                    
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Stack</div>
                    
                    {
                      stack.map((object, i) => {
                        return (
                          <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(isStackActive==i) && 'bg-blue-200'}`} onClick={()=>setIsStackActive(i)}>{object}</div>
                        )
                      })
                    }

                  </div>

                </div>
              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button>Stack</Button>
              </CardFooter>


          </TabsContent>

          </Card>

          
        </Tabs>

      </div>

      </Card>
    </div>

  );
}
