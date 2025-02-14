"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
// import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsTrigger } from "@/components/ui/tabs";
import { TabsList } from "@radix-ui/react-tabs";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import { AlertDialog, AlertDialogAction, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
// import { Label } from "@/components/ui/label"
// import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


export default function Home() {


  const [url, setUrl] = useState<string | undefined>();
  const [verified, setVerified] = useState<boolean | undefined>();
  const [jointPosOriginal, setJointPosOriginal] = useState([0,0,0,0,0,0,0,0]);
  const [jointPosNew, setJointPosNew] = useState([0,0,0,0,0,0]);
  const [armCoordsOriginal, setArmCoordsOriginal] = useState([0,0,0,0]);
  const [armCoordsNew, setArmCoordsNew] = useState([0,0,0,0]);
  const [objectActive, setObjectActive] = useState<number | undefined>();
  const [isStackActive, setIsStackActive] = useState<number | undefined>();
  const [stack, setStack] = useState<string[]>([]);
  const [stackingObjects, setStackingObjects] = useState<string[]>(['Pot','Cuboid', 'Cylinder', 'Prism', 'Bowl', 'Cup1', 'Cup0', 'Cup2', 'Cup3']);
  const [objectActiveManipulate, setObjectActiveManipulate] = useState<number | undefined>();
  const objectList = ['Cuboid', 'Pot', 'Cylinder', 'Prism', 'Bowl', 'Cup1', 'Cup0', 'Cup2', 'Cup3'];
  const predefPaths = ['Circle', 'Square', 'Hexagon', 'Heart'];
  const [activePath, setActivePath] = useState<number | undefined>();
  const [objMoveCoord, setObjMoveCoord] = useState([0,0,0]);

  useEffect(()=>{
    getPosition();
  }, [url])

  async function getPosition(){
    const res = await fetch(`http://${url}/getalljoints`)
    const data = await res.json();
    setJointPosOriginal(data.joint_positions);
    setJointPosNew(data.joint_positions);
  }

  function addToStack(){
    if (objectActive != undefined && stack.length < 5){
      setStack([String(stackingObjects[objectActive]), ...stack]);
      setStackingObjects(stackingObjects.filter((_, i) => i != objectActive));
    }
    setObjectActive(undefined);
  }

  function removeFromStack(){
    if (isStackActive != undefined){
      setStack(stack.filter((_, i) => i != isStackActive));
      setStackingObjects([...stackingObjects, stack[isStackActive]]);
    }
    setIsStackActive(undefined);
  }

  useEffect(()=>{
    console.log(jointPosOriginal);
  }, [jointPosOriginal]) ;

  
  async function verifyUrl(url:string){
    try{
      const res = await fetch(`http://${url}/verify`);
      const data = await res.json();
      if (data.message == 'InteractiveRobotics'){
        setUrl(url);
        setVerified(true);
      }else{
        setVerified(false);
      }
    }
    catch{
      setVerified(false);
    }
  }
  
  async function jointsCall(){
    console.log(url);
    await fetch(`http://${url}/alljoints`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        degree: jointPosNew
      }) 
    })
    setJointPosOriginal(jointPosNew);

  }

  async function coordinateCall(){
    await fetch(`http://${url}/movebycoordinates`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          l : [armCoordsNew[0], armCoordsNew[1], armCoordsNew[2]],
      }) 
    })
    setArmCoordsOriginal(armCoordsNew);
  }

  async function stackCall(){
    const revList = stack.slice().reverse();
    await fetch(`http://${url}/stacktheobjects`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          objects : revList,
      }) 
    })

  }

  async function pathCall(){
    if (activePath == undefined){
      return;
    }
    await fetch(`http://${url}/moveinpath`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          path : predefPaths[activePath].toLowerCase(),
      }) 
    })
  }

  async function objectMoveCall(){
    if (objectActiveManipulate == undefined){
      return;
    }
    await fetch(`http://${url}/moveobject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          object : objectList[objectActiveManipulate],
          l : [objMoveCoord[0], objMoveCoord[1], objMoveCoord[2]],
      }) 
    })
  }

  async function pickObjectCall() { 
    if (objectActiveManipulate == undefined){
      return;
    }
    await fetch(`http://${url}/pickup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          object : objectList[objectActiveManipulate],
      }) 
    })
  }

  async function dropObjectCall() { 
    await fetch(`http://${url}/drop`, {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          object : 1,
      })
    })
  }


  return (
    <div className="w-full flex items-center flex-col h-full">

      <AlertDialog open={ verified ? false : true}>

        <AlertDialogContent>

          <AlertDialogHeader>
            <AlertDialogTitle>Simulation Server URL</AlertDialogTitle>
            
              <AlertDialogDescription>
              Enter the URL of the machine running the simulation server. 
              It can be found at http://localhost:8000 on the machine running the server.
              <Input type='text' placeholder="192.168.1.1" id="ipaddr"/>
              {verified===false && <div className="text-red-500">Invalid URL</div>}
              </AlertDialogDescription>


            </AlertDialogHeader>

          
          <AlertDialogFooter>
            <AlertDialogAction onClick={() => {

             const ipInp = document.getElementById('ipaddr') as HTMLInputElement;
             verifyUrl(ipInp.value); 
            
            }}>Continue</AlertDialogAction>
          </AlertDialogFooter>

        </AlertDialogContent>

      </AlertDialog>



    <Card className="w-3/4 h-screen rounded-none">

      <div className="mx-auto p-8 border-b text-center">
        <h1 className="text-3xl font-bold">Interactive Robotics</h1>
        <p className="text-lg font-extralight">GUI for controlling the simulation of a robot</p>
      </div>

      <div className="space-y-4 px-16 text-lg my-2">

        <Tabs defaultValue="joint" className="w-full h-[75vh]">

          <TabsList className="grid grid-cols-5 bg-muted p-1 w-fit mx-auto">
            <TabsTrigger value="joint">Joint Control</TabsTrigger>
            <TabsTrigger value="arm">Arm Control</TabsTrigger>
            <TabsTrigger value="object">Object Control</TabsTrigger>
            <TabsTrigger value="stack">Stacking</TabsTrigger>
            <TabsTrigger value="macros">Macros</TabsTrigger>
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

                {['Joint 1', 'Joint 2', 'Joint 3','Joint 4','Joint 5','Joint 6'].map((joint, i) => {
                return (
                <div key={i} className="flex grid grid-cols-3 space-x-4 w-full ">
                  <div className="text-center text-base h-full align-middle flex flex-col justify-center">{joint}</div>
                  <div> 
                    <Input type='number' value={ jointPosNew[i] } onChange={(e) => setJointPosNew(jointPosNew.map((v, j) => {
                    if (j == i){
                      if (Number.isNaN(e.target.valueAsNumber)){
                        return 0;
                      }
                      return e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                  <div>
                  <Input type='number' value={jointPosNew[i] - jointPosOriginal[i]} onChange={(e) => setJointPosNew(jointPosNew.map((v, j) => {
                    if (j == i){
                      if (Number.isNaN(e.target.valueAsNumber)){
                        return jointPosOriginal[j];
                      }
                      return jointPosOriginal[j] + e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                </div>
                )})}

              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button onClick={() => jointsCall()}>Save and Move</Button>
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

                {['X Coord', 'Y Coord', 'Z Coord'].map((joint, i) => {
                return (

                <div key={i} className="flex grid grid-cols-3 space-x-4 w-full">
                  <div className="flex-1/6 text-center">{joint}</div>
                  <div>
                  <Input type='number' value={ armCoordsNew[i] } onChange={(e) => setArmCoordsNew(armCoordsNew.map((v, j) => {
                    if (j == i){
                      if (Number.isNaN(e.target.valueAsNumber)){
                        return 0;
                      }
                      return e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                  <div>
                  <Input type='number' value={armCoordsNew[i] - armCoordsOriginal[i]} onChange={(e) => setArmCoordsNew(armCoordsNew.map((v, j) => {
                    if (j == i){
                      if (Number.isNaN(e.target.valueAsNumber)){
                        return armCoordsOriginal[j];
                      }
                      return armCoordsOriginal[j] + e.target.valueAsNumber;
                    }
                    return v;
                  } )) } />
                  </div>
                </div>

                )})}

                {/* <div className="flex grid grid-cols-3 space-x-4 w-full">
                  <div className="flex-1/6 text-center">Grasp</div>
                  
                  <div>
                    <RadioGroup defaultValue="1" className="flex" onChange={(e) => console.log(e)}>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="1" id="option-one" />
                        <Label htmlFor="option-one">Open</Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="2" id="option-two" />
                        <Label htmlFor="option-two">Close</Label>
                      </div>
                    </RadioGroup>
                  </div>
                </div> */}

              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button onClick={coordinateCall}>Save and Move</Button>
              </CardFooter>

          </TabsContent>

          <TabsContent value="object" className="h-full">
              
              <CardContent className="w-full space-y-4">
              
              <div className="flex">

              <div className="flex flex-col w-5/12">
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Object</div>
                    <div className="h-[50vh] overflow-y-auto">
                    {
                      objectList.map((object, i) => {
                        return (
                            <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(objectActiveManipulate==i) && 'bg-blue-200'}`} onClick={()=>setObjectActiveManipulate(i)}>{object}</div>
                        )
                      })
                    }
                      </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-center space-x-4 text-xl font-semibold text-center">
                  <div>Position</div>
                </div>
                
                <Separator/>

                {['X Coord', 'Y Coord', 'Z Coord'].map((joint, i) => {
                return (

                <div key={i} className="flex grid grid-cols-2 space-x-4 w-full">
                  <div className="flex-1/6 text-center">{joint}</div>
                  <div>
                  <Input type='number' value={ objMoveCoord[i] } onChange={(e) => setObjMoveCoord(objMoveCoord.map((v, j) => {
                    
                    if (j == i){
                      if (Number.isNaN(e.target.valueAsNumber)){
                        return 0;
                      }
                      return e.target.valueAsNumber;
                    }

                    return v;
                  } )) } />
                  </div>
                  
                </div>

                )})}
              </div>
              

              </div>

              </CardContent>

              <CardFooter className="text-right justify-end flex space-x-4">
                <Button onClick={dropObjectCall}>Drop The Object</Button>
                <Button onClick={pickObjectCall}>Pick The Object</Button>
                <Button onClick={objectMoveCall}>Move the Object</Button>
              </CardFooter>

          </TabsContent>

          <TabsContent value="stack">
              
              <CardContent className="space-y-4 w-full">
                
                <div className="flex justify-evenly w-full h-[50vh]">
                  <div className="flex flex-col w-5/12">
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Object</div>
                    <div className="h-[50vh] overflow-y-auto">
                    {
                      stackingObjects.map((object, i) => {
                        return (
                            <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(objectActive==i) && 'bg-blue-200'}`} onClick={()=>setObjectActive(i)}>{object}</div>
                        )
                      })
                    }
                    </div>
                  </div>
                  <div className="flex flex-col h-full w-1/16 space-y-4 justify-center my-auto">
                    <Button onClick={addToStack}><ArrowRight/></Button>
                    <Button onClick={removeFromStack}><ArrowLeft/></Button>
                  </div>

                  <div className="flex flex-col w-5/12">
                    
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Stack</div>
                    <div className="h-[50vh] overflow-y-auto">
                    
                    {
                      stack.map((object, i) => {
                        return (
                          <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(isStackActive==i) && 'bg-blue-200'}`} onClick={()=>setIsStackActive(i)}>{object}</div>
                        )
                      })
                    }
                    </div>
                  </div>

                </div>
              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button onClick={()=>stackCall()}>Stack</Button>
              </CardFooter>


          </TabsContent>

          <TabsContent value="macros">
              
              <CardContent className="space-y-4 w-full">
                
                <div className="flex justify-evenly w-full h-[50vh]">
                  <div className="flex flex-col w-8/12">
                    <div className="text-xl font-semibold my-2 text-center space-y-2">Predefined Paths</div>
                    {
                      predefPaths.map((path, i) => {
                        return (
                            <div key={i} className={`flex-1/6 text-left border my-2 p-2 rounded-lg ${(activePath==i) && 'bg-blue-200'}`} onClick={()=>setActivePath(i)}>{path}</div>
                        )
                      })
                    }
                  </div>
                </div>
              </CardContent>

              <CardFooter className="text-right justify-end flex">
                <Button onClick={()=>pathCall()}>Run Macro</Button>
              </CardFooter>


          </TabsContent>
          
          </Card>

          
        </Tabs>

      </div>

      </Card>
    </div>

  );
}
