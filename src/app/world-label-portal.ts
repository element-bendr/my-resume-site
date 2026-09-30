import { createContext, type RefObject } from "react";

export const WorldLabelPortalContext = createContext<RefObject<HTMLElement | null> | null>(null);
