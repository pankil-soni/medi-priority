"use client";
import { NextUIProvider } from "@nextui-org/react";
import React from "react";

const AppProvider = ({ children }) => {
  return <NextUIProvider>{children}</NextUIProvider>;
};

export default AppProvider;
