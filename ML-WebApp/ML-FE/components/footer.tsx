import Image from "next/image";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="footer bg-neutral text-neutral-content p-5 ">
      <div className="flex justify-center ">
        <Image
          src="/images/ub-logo.jpg"
          alt="ub-logo"
          className="rounded-full"
          width={100}
          height={100}
        />
      </div>

      <nav>
        <h6 className="footer-title">Team members</h6>
        <Link href={"/about"} className="link link-hover">
          About us
        </Link>
        <a className="link link-hover">Contact</a>
      </nav>
      <nav>
        <h6 className="footer-title">Resources</h6>
        <a className="link link-hover">Terms of use</a>
        <Link
          href={"https://github.com/MariaMonserratM/Capstone_bike"}
          className="link link-hover"
        >
          Repository
        </Link>
      </nav>
    </footer>
  );
}
