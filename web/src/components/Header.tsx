import { Sprout } from "lucide-react";
import { Button } from "./ui/button";
import { Link } from "react-router-dom";

type HeaderProps = {
  showTryIt?: boolean;
};

function Header({ showTryIt = false }: HeaderProps) {
  return (
    <header className="p-4 px-6 border-b-2 border-black flex justify-between">
      <div className="text-2xl font-bold flex items-center gap-1">
        <Link to="/" className="flex items-center gap-1">
          Sproute
          <Sprout className="text-green-600" />
        </Link>
      </div>
      <div className="space-x-4">
        <Button variant="ghost" className="text-green-600" asChild>
          <Link to="/rewards">Rewards</Link>
        </Button>
        {showTryIt && (
          <Button
            variant="default"
            className="bg-green-600 hover:bg-green-800"
            asChild
          >
            <Link to="/planner">Try it out!</Link>
          </Button>
        )}
      </div>
    </header>
  );
}

export default Header;
