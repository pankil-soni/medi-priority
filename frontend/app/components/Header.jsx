"use client";
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
} from "@nextui-org/react";
import { motion } from "framer-motion";

export default function Header() {
  return (
    <Navbar>
      <NavbarBrand>
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Link href="/" className="font-bold text-inherit">
            Medical Assistant
          </Link>
        </motion.div>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem>
          <Link href="/">Home</Link>
        </NavbarItem>
        <NavbarItem>
          <Link href="/questionnaire">Questionnaire</Link>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
