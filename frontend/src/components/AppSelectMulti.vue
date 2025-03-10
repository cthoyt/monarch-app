<!--
  custom multi select

  references:
  https://www.w3.org/TR/2021/NOTE-wai-aria-practices-1.2-20211129/examples/listbox/listbox-rearrangeable.html
  https://w3c.github.io/aria/#aria-multiselectable
  https://developer.mozilla.org/en-US/docs/Web/API/Element/ariaMultiSelectable
  https://vuetifyjs.com/en/components/selects/
  https://www.downshift-js.com/use-select
-->

<template>
  <div class="select-multi">
    <!-- select button box -->
    <component
      :is="design === 'small' ? 'AppButton' : 'button'"
      :id="`select-${id}`"
      ref="anchor"
      :class="[
        {
          notification: !allSelected && !noneSelected,
          box: design === 'normal',
        },
      ]"
      :aria-label="name"
      :aria-expanded="expanded"
      :aria-controls="`list-${id}`"
      aria-haspopup="listbox"
      icon="filter"
      design="small"
      @click="onClick"
      @keydown="onKeydown"
      @blur="onBlur"
    >
      <template v-if="design === 'normal'">
        <span class="box-label">
          {{ name }}
          <span class="box-more">
            <template v-if="selected.length === 0">none selected</template>
            <template v-else-if="selected.length === options.length">
              all selected
            </template>
            <template v-else-if="selected.length === 1">
              {{ options[selected[0]]?.label || options[selected[0]]?.id }}
            </template>
            <template v-else>{{ selected.length }} selected</template>
          </span>
        </span>
        <AppIcon
          class="button-icon"
          :icon="expanded ? 'angle-up' : 'angle-down'"
        />
      </template>
    </component>

    <!-- options list -->
    <Teleport to="body">
      <div
        v-if="expanded"
        :id="`list-${id}`"
        ref="dropdown"
        class="list"
        role="listbox"
        :aria-labelledby="`select-${id}`"
        :aria-activedescendant="
          expanded ? `option-${id}-${highlighted}` : undefined
        "
        tabindex="0"
        :style="style"
      >
        <!-- select all -->
        <div
          :id="`option-${id}--1`"
          :class="['option', { highlighted: highlighted === -1 }]"
          role="option"
          :aria-label="allSelected ? 'Deselect all' : 'Select all'"
          :aria-selected="allSelected"
          tabindex="0"
          @click="() => toggleSelect(-1)"
          @mousedown.prevent=""
          @focusin="() => null"
          @keydown="() => null"
        >
          <AppIcon
            :icon="allSelected ? 'square-check' : 'square'"
            class="option-check"
          />
          <span class="option-label truncate">All</span>
          <span class="option-count"></span>
        </div>

        <div class="option-spacer" aria-hidden="true"></div>

        <!-- options -->
        <div
          v-for="(option, index) in options"
          :id="`option-${id}-${index}`"
          :key="index"
          v-tooltip="option.tooltip"
          :class="['option', { highlighted: highlighted === -1 }]"
          role="option"
          :aria-selected="selected.includes(index)"
          tabindex="0"
          @click="(event) => toggleSelect(index, event.shiftKey)"
          @mousedown.prevent=""
          @focusin="() => null"
          @keydown="() => null"
        >
          <AppIcon
            :icon="selected.includes(index) ? 'square-check' : 'square'"
            class="option-check"
          />
          <AppIcon v-if="option.icon" :icon="option.icon" class="option-icon" />
          <span class="option-label truncate">
            {{ option.label || option.id }}
          </span>
          <span
            v-if="option.count !== undefined && showCounts"
            class="option-count"
          >
            {{ option.count.toLocaleString() }}
          </span>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script lang="ts">
export type Option = {
  /** unique id used in state of select */
  id: string;
  /** display label */
  label?: string;
  /** icon */
  icon?: string;
  /** count col */
  count?: number;
  /** tooltip on hover */
  tooltip?: string;
};

export type Options = Option[];
</script>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";
import { isEqual, uniqueId } from "lodash";
import { useFloating } from "@/util/composables";
import { wrap } from "@/util/math";

type Props = {
  /** two-way bound selected items state */
  modelValue: Options;
  /** name of the field */
  name: string;
  /** list of options to show */
  options: Options;
  /** visual design */
  design?: "normal" | "small";
  /** whether to show counts for each option */
  showCounts?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  design: "normal",
  showCounts: true,
});

type Emits = {
  /** two-way bound selected items state */
  "update:modelValue": [Options];
  /** whether specific items are selected, and not all/none selected */
  partial: [boolean];
  /** when value changed */
  input: [];
  /** when value change "submitted"/"committed" by user */
  change: [Options];
};

const emit = defineEmits<Emits>();

/** unique id for instance of component */
const id = uniqueId();
/** whether dropdown is open */
const expanded = ref(false);
/** array of indices of selected options */
const selected = ref<number[]>([]);
/** selected state when dropdown was opened */
const original = ref<number[]>([]);
/** index of option that is highlighted (keyboard controls) */
const highlighted = ref(0);

/** anchor element */
const anchor = ref();
/** dropdown element */
const dropdown = ref();
/** get dropdown position */
const { calculate, style } = useFloating(
  computed(() => anchor.value?.button || anchor.value),
  dropdown,
);
/** recompute position after opened */
watch(expanded, async () => {
  await nextTick();
  if (expanded.value) calculate();
});

function open() {
  /** open dropdown */
  expanded.value = true;
  /** auto highlight first selected option */
  highlighted.value = selected.value[0] || 0;
  /** remember selected state when opened */
  original.value = [...selected.value];
}

function close() {
  /** close dropdown */
  expanded.value = false;
  /** emit change, if value is different from when dropdown first opened */
  if (!isEqual(selected.value, original.value)) emit("change", getModel());
  /** also update original value here in case e.g. user presses esc then blurs */
  original.value = [...selected.value];
}

/** when button clicked */
function onClick() {
  /** toggle dropdown */
  expanded.value ? close() : open();
  /** https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#clicking_and_focus */
  document.querySelector<HTMLElement>(`#select-${id}`)?.focus();
}

/** when button blurred */
function onBlur() {
  close();
}

/** when user presses key on button */
function onKeydown(event: KeyboardEvent) {
  /** arrow/home/end keys */
  if (
    ["ArrowUp", "ArrowDown", "Home", "End"].includes(event.key) &&
    expanded.value
  ) {
    /** prevent page scroll */
    event.preventDefault();

    /** move value up/down */
    let index = highlighted.value;
    if (event.key === "ArrowUp") index--;
    if (event.key === "ArrowDown") index++;
    if (event.key === "Home") index = 0;
    if (event.key === "End") index = props.options.length - 1;

    /** update highlighted, wrapping beyond -1 or options length */
    highlighted.value = wrap(index, -1, props.options.length - 1);
  }

  /** enter key to de/select highlighted option */
  if (expanded.value && (event.key === "Enter" || event.key === " ")) {
    /** prevent browser re-clicking open button */
    event.preventDefault();
    toggleSelect(highlighted.value);
  }

  /** esc key to close dropdown */
  if (expanded.value && event.key === "Escape") close();
}

/** get new selected option indices from model value */
function getSelected(): number[] {
  return props.options
    .map((option, index) =>
      props.modelValue.find((model) => option.id === model.id) ? index : -1,
    )
    .filter((index) => index !== -1);
}

/** get new model value from selected option indices */
function getModel(): Options {
  return props.options.filter((_, index) => selected.value.includes(index));
}

/** select or deselect option(s) */
function toggleSelect(index = -1, solo = false) {
  /**
   * if all selected, and individual option clicked, start by selecting just
   * clicked
   */
  if (index !== -1 && allSelected.value) solo = true;

  /** toggle all options */
  if (index === -1) {
    if (allSelected.value) selected.value = [];
    else
      selected.value = Array(props.options.length)
        .fill(0)
        .map((_, index) => index);
  } else if (solo) {
    /** solo/un-solo one option */
    if (isEqual(selected.value, [index]))
      selected.value = Array(props.options.length)
        .fill(0)
        .map((_, index) => index);
    else selected.value = [index];
  } else {
    /** toggle one option */
    if (selected.value.includes(index))
      selected.value = selected.value.filter((value) => value !== index);
    else selected.value.push(index);
  }

  /** keep in order for easy comparison */
  selected.value.sort();
  /** emit input event for listening for only user-originated inputs */
  emit("input");
}

/** when model changes, update selected indices */
watch(
  () => props.modelValue,
  () => {
    /** avoid infinite rerenders */
    if (!isEqual(selected.value, getSelected())) selected.value = getSelected();
  },
  { deep: true, immediate: true },
);

/** when selected index changes, update model */
watch(selected, () => emit("update:modelValue", getModel()), { deep: true });

/** when highlighted index changes */
watch(
  highlighted,
  () =>
    /** scroll to highlighted in dropdown */
    document
      .querySelector(`#option-${id}-${highlighted.value} > *`)
      ?.scrollIntoView({ block: "nearest" }),
);

/** are all options selected */
const allSelected = computed(
  () => selected.value.length === props.options.length,
);

/** are no options selected */
const noneSelected = computed(() => !selected.value.length);

/** update partial status */
watch(
  [allSelected, noneSelected],
  () => {
    emit("partial", !(allSelected.value || noneSelected.value));
  },
  { immediate: true },
);
</script>

<style lang="scss" scoped>
.select-multi {
  position: relative;
  max-width: 100%;
  text-transform: capitalize;
}

.box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 5px 10px;
  gap: 10px;
  border-radius: $rounded;
  background: $light-gray;
}

.box-label {
  flex-grow: 1;
  text-align: left;
}

.box-more {
  margin-left: 10px;
  color: $dark-gray;
}

.list {
  z-index: 1020;
  max-width: 90vw;
  max-height: 300px;
  overflow-x: auto;
  overflow-y: auto;
  background: $white;
  box-shadow: $shadow;
}

.option {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 7.5px;
  gap: 10px;
  cursor: pointer;
  transition: background $fast;
}

.option:hover,
.option.highlighted {
  background: $light-gray;
}

.option-spacer {
  height: 10px;
}

.option-check {
  color: $theme;
  font-size: 1.2rem;
}

.option-icon {
  color: $dark-gray;
  font-size: 1.2em;
}

.option-label {
  flex-grow: 1;
  justify-content: flex-start;
  overflow-x: hidden;
}

.option-count {
  justify-content: flex-end;
  color: $gray;
}
</style>
