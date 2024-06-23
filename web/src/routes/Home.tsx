import Header from "../components/Header";
import bearUrl from "../assets/bear.png";

function Home() {
  return (
    <>
      <Header showTryIt />
      <div className="flex justify-center items-center my-32 px-20">
        <div className="flex flex-col items-center">
          <h1 className="text-6xl font-bold text-center">
            Explore the world, <br />
            Preserve the{" "}
            <span className="text-green-600 italic font-extrabold">Earth</span>.
          </h1>
          <p className="mt-8 text-lg text-black max-w-2xl text-center">
            The ultimate AI-powered trip planner that prioritizes sustainable
            and eco-friendly travel options. Plan your dream vacation while
            minimizing your carbon footprint.
          </p>
        </div>
        {/* <img src={bearUrl} className="h-64"></img> */}
      </div>
      <div className="mx-auto bg-white bg-opacity-80 p-8 rounded-lg shadow-lg max-w-3xl text-center">
        <div className="flex flex-col md:flex-row justify-around gap-10 md:gap-6 px-8">
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
              Our advanced AI ensures personalized itineraries tailored to your
              preferences and needs.
            </p>
          </div>
          <div className="md:w-1/3">
            <h3 className="text-2xl font-bold mb-2">Customizable Itenerary</h3>
            <p>Base your travel itenerary on your interests.</p>
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;
