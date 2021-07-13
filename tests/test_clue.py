from arxtools.clue import parse_clue


def test_parse_shared_clue_with_note():
    html='''
<tr>
  <td valign="top">42</td>
  <td valign="top"><b>Clue Title</b></td>
  <td valign="top">
    Clue Text
    <div class="well">
      <br/>&nbsp;<br/>
      <strong>Clue Tags: </strong>foo, bar, baz
      <br/>&nbsp;<br/>
      This clue was shared with you by Alice, who noted: Clue Share Note
    </div>
  </td>
</tr>
'''
    clue = parse_clue(html)
    assert 42 == clue.id
    assert 'Clue Title' == clue.title
    assert 'Clue Text' == clue.text
    assert ['foo', 'bar', 'baz'] == clue.tags
    assert 'Alice' == clue.source
    assert 'Clue Share Note' == clue.share_note

def test_parse_briefed_clue():
    html='''
<tr>
  <td valign="top">42</td>
  <td valign="top"><b>Clue Title</b></td>
  <td valign="top">
    Clue Text
    <div class="well">
      <br/>&nbsp;<br/>
      <strong>Clue Tags: </strong>foo, bar, baz
    </div>
  </td>
</tr>
'''
    clue = parse_clue(html)
    assert clue.source is None
    assert clue.share_note is None

def test_parse_investigation_clue():
    html='''
<tr>
  <td valign="top">42</td>
  <td valign="top"><b>Clue Title</b></td>
  <td valign="top">
    Clue Text
    <div class="well">
      <br/>&nbsp;<br/>
      <strong>Clue Tags: </strong>foo, bar, baz
      <br/>&nbsp;<br/>
      Your investigation has discovered this!
    </div>
  </td>
</tr>
'''
    clue = parse_clue(html)
    assert 'investigation' == clue.source
    assert clue.share_note is None

def test_parse_with_no_meta_info():
    html='''
<tr>
  <td valign="top">42</td>
  <td valign="top"><b>Clue Title</b></td>
  <td valign="top">
    Clue Text
  </td>
</tr>
'''
    clue = parse_clue(html)
    assert clue.source is None
    assert clue.share_note is None
