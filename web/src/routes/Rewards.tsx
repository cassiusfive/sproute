import Header from "./../components/Header";
import creditCardImage from "../assets/credit-card-image.png"; // Adjust the path as necessary

function Rewards() {
  return (
    <>
      <Header />
      <div className="bg-gradient-to-r from-black via-gray-900 to-green-800 text-white min-h-screen flex flex-col items-center">
        <div className="max-w-5xl mx-auto p-6 flex flex-col md:flex-row items-center mt-16">
          <div className="md:w-1/2 text-center md:text-left mb-8 md:mb-0">
            <h1 className="text-5xl font-bold mb-6">
              FINALLY.
              <br />
              A CARD THAT LETS YOU EARN POINTS ON{" "}
              <span className="text-green-500">SUSTAINABLE TRAVEL</span>.
            </h1>
            <p className="text-xl mb-6">
              The Sproute Travel Credit Card rewards you for making sustainable travel choices. Earn points when you stay at eco-friendly hotels, dine at sustainable restaurants, use public transportation, and more. Use your points towards future travels and make a positive impact on the environment.
            </p>
            <div className="text-4xl font-bold mb-4">$0</div>
            <div className="text-lg mb-4">ANNUAL FEE</div>
            <div className="flex flex-col gap-2 text-lg mb-6">
              <div>1X points on sustainable hotels</div>
              <div>2X points on public transportation</div>
              <div>3X points on eco-friendly restaurants</div>
            </div>
            <button className="bg-white text-black py-3 px-6 rounded-lg font-semibold hover:bg-gray-200">
              Join the Waitlist
            </button>
          </div>
          <div className="md:w-1/2 flex justify-center">
            <img src={creditCardImage} alt="Credit Card" className="w-80" />
          </div>
        </div>
      </div>
    </>
  );
}

export default Rewards;
