import type { Ref } from "vue";

import { computed, ref, watch } from "vue";

export function useStepperInteractions(stepperRef: Ref) {
  const stepCount = computed(() => {
    const stepperEl = stepperRef.value?.$el as HTMLElement | undefined;
    if (!stepperEl) return 0;
    return stepperEl.querySelectorAll(".v-stepper-vertical-item").length;
  });

  const manualInteractions = ref<boolean[]>([]);

  watch(
    stepCount,
    (newStepCount) => {
      manualInteractions.value = Array(
        newStepCount > 0 ? newStepCount - 1 : 0
      ).fill(false);
    },
    { once: true }
  );

  async function interact(
    step: number,
    interaction: Promise<void> | (() => void)
  ) {
    manualInteractions.value[step - 1] = true;
    if (interaction instanceof Promise) {
      await interaction;
    } else {
      interaction();
    }
  }

  return { stepCount, manualInteractions, interact };
}
