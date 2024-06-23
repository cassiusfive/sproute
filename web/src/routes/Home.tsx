import Footer from "../components/Footer";
import Header from "../components/Header";
import { Flower } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";

function Home() {
  return (
    <>
      <div className="">
        <Header showTryIt />
        <div className="flex flex-col items-center my-44">
          <h1 className="text-6xl font-bold text-center">
            Explore the world, <br />
            Preserve the{" "}
            <span className="text-green-600 italic font-extrabold">Earth</span>.
          </h1>
          <p className="mt-4 text-lg text-secondary-foreground max-w-2xl text-center">
            Your ultimate AI-powered trip planner that prioritizes sustainable
            and eco-friendly travel options. Plan your dream vacation while
            minimizing your carbon footprint.
          </p>
          <Button
            variant="default"
            className="bg-green-600 hover:bg-green-800 mt-12"
            asChild
          >
            <Link to="/planner">Start Planning!</Link>
          </Button>
        </div>
        <div className="mt-8 mx-auto bg-white bg-opacity-80 p-8 rounded-lg shadow-lg max-w-3xl text-center border-2">
          <h2 className="text-4xl font-semibold mb-6">Why Choose Us?</h2>
          <div className="flex flex-col md:flex-row justify-around gap-10 md:gap-6">
            <div className="md:w-1/3">
              <h3 className="text-2xl font-bold mb-2">Eco-Friendly Choices</h3>
              <p>
                We prioritize sustainable travel options to help you reduce your
                environmental impact.
              </p>
            </div>
            <div className="md:w-1/3">
              <h3 className="text-2xl font-bold mb-2">AI-Powered Planning</h3>
              <p>
                Our advanced AI ensures personalized itineraries tailored to
                your preferences and needs.
              </p>
            </div>
            <div className="md:w-1/3">
              <h3 className="text-2xl font-bold mb-2">
                Customizable Itenerary
              </h3>
              <p>Base your travel itenerary on your interests.</p>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default Home;
