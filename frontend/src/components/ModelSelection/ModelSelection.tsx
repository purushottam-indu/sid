import { Dropdown, DropdownMenuItemType, IDropdownStyles, IDropdownOption } from "@fluentui/react/lib/Dropdown";

interface Props {
    selectedModel: IDropdownOption | undefined;
    onChangeModel: (event: React.FormEvent<HTMLDivElement>, item: IDropdownOption | undefined) => void;
    disabled: boolean;
}

const options: IDropdownOption[] = [
    { key: "GPT3.5", text: "GPT 3.5" },
    { key: "GPT4", text: "GPT 4" }
];

const dropdownStyles: Partial<IDropdownStyles> = {
    dropdown: { minWidth: "6rem" }
};

export const ModelSelection = ({ selectedModel, onChangeModel, disabled }: Props) => {
    return (
        <Dropdown
            placeholder="Select Model"
            disabled={disabled}
            options={options}
            onChange={onChangeModel}
            selectedKey={selectedModel?.key}
            styles={dropdownStyles}
        />
    );
};
