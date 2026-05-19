import { render, screen } from "@testing-library/react";
import MessageCompose from "../components/MessageCompose";

test("renders compose form", () => {
  render(<MessageCompose />);
  expect(screen.getByText("Compose")).toBeInTheDocument();
});
