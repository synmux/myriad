"""Tests for the matching rules in scan_broken.py.

Run with: uv run python -m unittest test_scan_broken -v
"""

import unittest
from datetime import UTC, datetime

from scan_broken import (
    Conversation,
    Fetch,
    QueryParams,
    cleanup_reason,
    list_conversations,
    structured_text,
)

NOW = datetime(2026, 11, 13, 2, 0, tzinfo=UTC)
MONTHS_AGO = "2026-04-13T20:10:53.066117Z"
ONE_HOUR_AGO = "2026-11-13T01:00:00Z"


def conversation(**overrides: object) -> Conversation:
    """A finished, healthy conversation row, with the given fields replaced."""
    healthy: Conversation = {
        "id": "example",
        "status": "completed",
        "home_step": "ready",
        "created_at": MONTHS_AGO,
        "discarded": False,
        "structured": {"title": "Example", "overview": "A real summary."},
    }
    return healthy | overrides


NO_SUMMARY = {"title": "Recording · 3:56 PM", "overview": ""}


class StatusNeverCompleted(unittest.TestCase):
    def test_old_merging_conversation_is_broken(self) -> None:
        self.assertEqual(
            cleanup_reason(conversation(status="merging"), NOW), "status is merging"
        )

    def test_old_processing_conversation_is_broken(self) -> None:
        self.assertEqual(
            cleanup_reason(conversation(status="processing"), NOW),
            "status is processing",
        )

    def test_old_in_progress_conversation_is_broken(self) -> None:
        self.assertEqual(
            cleanup_reason(conversation(status="in_progress"), NOW),
            "status is in_progress",
        )

    def test_recording_still_under_way_is_not_broken(self) -> None:
        live_recording = conversation(status="in_progress", created_at=ONE_HOUR_AGO)
        self.assertIsNone(cleanup_reason(live_recording, NOW))

    def test_conversation_that_just_finished_recording_is_not_broken(self) -> None:
        being_processed = conversation(status="processing", created_at=ONE_HOUR_AGO)
        self.assertIsNone(cleanup_reason(being_processed, NOW))


class CompletedButSummaryNeverArrived(unittest.TestCase):
    def test_old_conversation_still_writing_notes_is_broken(self) -> None:
        self.assertEqual(
            cleanup_reason(conversation(home_step="writing_notes"), NOW),
            "completed but still writing_notes",
        )

    def test_old_conversation_still_transcribing_is_broken(self) -> None:
        self.assertEqual(
            cleanup_reason(conversation(home_step="transcribing"), NOW),
            "completed but still transcribing",
        )

    def test_recent_conversation_still_writing_notes_is_not_broken(self) -> None:
        summary_pending = conversation(
            home_step="writing_notes", created_at=ONE_HOUR_AGO
        )
        self.assertIsNone(cleanup_reason(summary_pending, NOW))


class FinishedConversations(unittest.TestCase):
    def test_ready_conversation_is_not_broken(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(), NOW))

    def test_noise_conversation_is_not_broken(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(home_step="noise"), NOW))

    def test_empty_discarded_capture_marked_failed_is_not_broken(self) -> None:
        self.assertIsNone(
            cleanup_reason(conversation(home_step="failed", discarded=True), NOW)
        )

    def test_conversation_without_a_home_step_is_not_broken(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(home_step=None), NOW))


class DiscardedConversations(unittest.TestCase):
    def test_discarded_conversation_is_left_alone_by_default(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(discarded=True), NOW))

    def test_discarded_conversation_matches_when_discarded_cleanup_is_requested(
        self,
    ) -> None:
        self.assertEqual(
            cleanup_reason(conversation(discarded=True), NOW, include_discarded=True),
            "discarded",
        )

    def test_recently_discarded_conversation_is_left_alone_even_when_requested(
        self,
    ) -> None:
        still_settling = conversation(discarded=True, created_at=ONE_HOUR_AGO)
        self.assertIsNone(cleanup_reason(still_settling, NOW, include_discarded=True))

    def test_kept_conversation_is_not_matched_by_discarded_cleanup(self) -> None:
        self.assertIsNone(
            cleanup_reason(conversation(discarded=False), NOW, include_discarded=True)
        )

    def test_stuck_status_is_reported_ahead_of_discarded(self) -> None:
        stuck_and_discarded = conversation(status="processing", discarded=True)
        self.assertEqual(
            cleanup_reason(stuck_and_discarded, NOW, include_discarded=True),
            "status is processing",
        )


class ConversationsWithoutASummary(unittest.TestCase):
    def test_conversation_without_a_summary_is_left_alone_by_default(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(structured=NO_SUMMARY), NOW))

    def test_conversation_without_a_summary_matches_when_requested(self) -> None:
        self.assertEqual(
            cleanup_reason(
                conversation(structured=NO_SUMMARY), NOW, include_no_summary=True
            ),
            "no summary",
        )

    def test_whitespace_only_summary_counts_as_no_summary(self) -> None:
        blank = conversation(structured={"title": "Example", "overview": "  \n"})
        self.assertEqual(
            cleanup_reason(blank, NOW, include_no_summary=True), "no summary"
        )

    def test_conversation_missing_its_structured_block_counts_as_no_summary(
        self,
    ) -> None:
        self.assertEqual(
            cleanup_reason(conversation(structured=None), NOW, include_no_summary=True),
            "no summary",
        )

    def test_conversation_with_a_summary_is_not_matched(self) -> None:
        self.assertIsNone(cleanup_reason(conversation(), NOW, include_no_summary=True))

    def test_recent_conversation_without_a_summary_is_left_alone_even_when_requested(
        self,
    ) -> None:
        summary_pending = conversation(structured=NO_SUMMARY, created_at=ONE_HOUR_AGO)
        self.assertIsNone(cleanup_reason(summary_pending, NOW, include_no_summary=True))

    def test_discarded_conversation_without_a_summary_is_left_to_the_discarded_option(
        self,
    ) -> None:
        discarded_and_blank = conversation(structured=NO_SUMMARY, discarded=True)
        self.assertIsNone(
            cleanup_reason(discarded_and_blank, NOW, include_no_summary=True)
        )


class StructuredText(unittest.TestCase):
    def test_field_is_read_from_the_structured_block(self) -> None:
        self.assertEqual(structured_text(conversation(), "title"), "Example")

    def test_missing_or_null_block_or_field_reads_as_empty_text(self) -> None:
        for row in (
            conversation(structured=None),
            conversation(structured={}),
            conversation(structured={"title": None}),
            {"id": "no-structured-block"},
        ):
            with self.subTest(row=row):
                self.assertEqual(structured_text(row, "title"), "")


class Timestamps(unittest.TestCase):
    def test_timestamp_without_a_timezone_is_read_as_utc(self) -> None:
        twenty_five_hours_ago = conversation(
            status="processing", created_at="2026-11-12T01:00:00"
        )
        self.assertEqual(
            cleanup_reason(twenty_five_hours_ago, NOW), "status is processing"
        )

    def test_conversation_exactly_at_the_age_limit_is_not_broken(self) -> None:
        twenty_four_hours_ago = conversation(
            status="processing", created_at="2026-11-12T02:00:00+00:00"
        )
        self.assertIsNone(cleanup_reason(twenty_four_hours_ago, NOW))


def numbered_conversations(count: int) -> list[Conversation]:
    """Conversations one minute apart, so every `created_at` is distinct."""
    return [
        {
            "id": f"conversation-{number}",
            "created_at": f"2026-05-01T{number // 60:02d}:{number % 60:02d}:00.000000Z",
        }
        for number in range(count)
    ]


def omi_list_server(
    rows: list[Conversation],
    rows_per_response: int | None = None,
    inclusive_end_date: bool = True,
) -> Fetch:
    """
    Serve `rows` the way the Omi list does: newest first, filtered by `end_date`.

    Like the real server, it runs out of read budget on any offset and returns
    an empty truncated page. `rows_per_response` truncates every larger page.
    """

    def fetch(params: QueryParams) -> tuple[list[Conversation], bool]:
        if params.get("offset"):
            return [], True
        end_date = params.get("end_date")
        matching = [
            row
            for row in rows
            if end_date is None
            or row["created_at"] < end_date
            or (inclusive_end_date and row["created_at"] == end_date)
        ]
        matching.sort(key=lambda row: row["created_at"], reverse=True)
        page = matching[: int(params["limit"])]
        if rows_per_response is not None and len(page) > rows_per_response:
            return page[:rows_per_response], True
        return page, False

    return fetch


class ListingConversations(unittest.TestCase):
    def test_every_conversation_is_listed_once_when_the_list_spans_many_pages(
        self,
    ) -> None:
        rows = numbered_conversations(250)
        listed = [
            row["id"] for row in list_conversations("completed", omi_list_server(rows))
        ]
        self.assertCountEqual(listed, [row["id"] for row in rows])

    def test_conversations_sharing_a_timestamp_across_a_page_break_are_all_listed(
        self,
    ) -> None:
        rows = numbered_conversations(150)
        for row in rows[45:55]:
            row["created_at"] = rows[45]["created_at"]
        listed = [
            row["id"] for row in list_conversations("completed", omi_list_server(rows))
        ]
        self.assertCountEqual(listed, [row["id"] for row in rows])

    def test_every_conversation_is_listed_when_the_server_truncates_each_page(
        self,
    ) -> None:
        rows = numbered_conversations(250)
        truncating_server = omi_list_server(rows, rows_per_response=30)
        listed = [
            row["id"] for row in list_conversations("completed", truncating_server)
        ]
        self.assertCountEqual(listed, [row["id"] for row in rows])

    def test_status_with_no_conversations_lists_nothing(self) -> None:
        self.assertEqual(list(list_conversations("merging", omi_list_server([]))), [])

    def test_truncated_page_that_brings_nothing_new_stops_the_scan_loudly(self) -> None:
        def exhausted_server(
            params: QueryParams,
        ) -> tuple[list[Conversation], bool]:
            return [], True

        with self.assertRaises(RuntimeError):
            list(list_conversations("completed", exhausted_server))

    def test_server_that_drops_the_boundary_conversation_stops_the_scan_loudly(
        self,
    ) -> None:
        exclusive_server = omi_list_server(
            numbered_conversations(250), inclusive_end_date=False
        )
        with self.assertRaises(RuntimeError):
            list(list_conversations("completed", exclusive_server))


if __name__ == "__main__":
    unittest.main()
