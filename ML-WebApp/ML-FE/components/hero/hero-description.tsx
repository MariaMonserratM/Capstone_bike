import Link from "next/link";

export default function HeroDescription() {
  return (
    <div className={`text-center ml-6`}>
      <h1 className="text-4xl font-bold text-white">Welcome to Barcelona!</h1>
      <p className={`mt-4 text-lg text-gray-300 font-semibold `}>
        <span> Discover amazing things here ... </span>
        <span> Fancy a bike? 😉</span>
      </p>

      <Link href={"/map"}>
        <button className="mt-8 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-extrabold">
          Get Started
        </button>
      </Link>
    </div>
  );
}
