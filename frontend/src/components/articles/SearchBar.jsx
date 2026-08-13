import {
  Search,
  X,
} from "lucide-react";

export default function SearchBar({
  value,
  onChange,
  onSubmit,
  onClear,
  semantic = false,
  placeholder,
}) {
  return (
    <form
      className="search-bar"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit?.();
      }}
    >
      <Search
        size={19}
        className="search-icon"
      />

      <input
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        placeholder={
          placeholder ||
          "Search for news, stories or topics..."
        }
      />

      {value && (
        <button
          type="button"
          className="search-clear"
          onClick={onClear}
        >
          <X size={16} />
        </button>
      )}

      <button
        type="submit"
        className="search-submit"
      >
        Search
      </button>
    </form>
  );
}