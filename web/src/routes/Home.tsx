import Header from "../components/Header";

function Home() {
  return (
    <>
      <Header />
      <div className="flex flex-col items-center">
        <h1 className="mt-16 text-6xl font-bold text-center">
          Explore the world, <br />
          Preserve the{" "}
          <span className="text-green-600 italic font-extrabold">Earth</span>.
        </h1>
        <p className="mt-8">
          Lorem Ipsum Lorem Ipsum Lorem IpsumLorem Ipsum Lorem Ipsum
        </p>
      </div>
    </>
  );
}

export default Home;
