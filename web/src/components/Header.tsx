import { Sprout } from "lucide-react";
import { Button } from "./ui/button";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="p-4 px-6 border-b-2 flex justify-between">
      <div className="text-2xl font-bold flex items-center gap-1">
        Sproute
        <Sprout className="text-green-600" />
      </div>
      <div>
        <Button variant="default" className="bg-green-600 hover:bg-green-800">
          Try it out!
        </Button>
      </div>
    </header>
  );
}

export default Header;
