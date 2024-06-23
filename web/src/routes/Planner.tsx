import Header from "./../components/Header";
import { ProfileForm } from "./../components/ProfileForm";

function Planner() {
  return (
    <>
      <Header />
      <div className="mt-4">
        <ProfileForm />
      </div>
    </>
  );
}

export default Planner;
